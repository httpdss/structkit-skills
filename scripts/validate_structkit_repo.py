#!/usr/bin/env python3
"""Validate a StructKit skill/template repository."""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

REQUIRED_FRONTMATTER = {"name", "description", "version"}
PATTERNS = [
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"(?i)(api[_-]?key|token|secret)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{24,}"),
]


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError(f"{path}: unterminated YAML frontmatter")
    data: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.startswith(" ") or line.startswith("#"):
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip().strip('"')
    return data


def validate_skill_files(root: Path) -> list[str]:
    errors: list[str] = []
    skill_files = list(root.glob("**/SKILL.md"))
    if not skill_files:
        return ["No SKILL.md files found"]
    for path in skill_files:
        try:
            fm = parse_frontmatter(path)
            missing = REQUIRED_FRONTMATTER - set(fm)
            if missing:
                errors.append(f"{path}: missing frontmatter keys: {sorted(missing)}")
        except Exception as exc:
            errors.append(str(exc))
    return errors


def validate_yaml_parse(paths: list[Path]) -> list[str]:
    errors: list[str] = []
    try:
        import yaml  # type: ignore
    except Exception:
        print("PyYAML not installed; skipping generic YAML parse check")
        return errors
    for path in paths:
        try:
            yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{path}: YAML parse failed: {exc}")
    return errors


def validate_with_structkit(paths: list[Path]) -> list[str]:
    errors: list[str] = []
    exe = shutil.which("structkit")
    if not exe:
        print("structkit CLI not found; skipping structkit validate")
        return errors
    for path in paths:
        result = subprocess.run(
            [exe, "validate", str(path)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        if result.returncode != 0:
            errors.append(f"{path}: structkit validate failed:\n{result.stdout}")
    return errors


def scan_for_sensitive_placeholders(root: Path) -> list[str]:
    errors: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in PATTERNS:
            if pattern.search(text):
                errors.append(f"{path}: possible secret-like value found")
    return errors


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    struct_files = sorted(root.glob("**/*.struct.yaml")) + sorted(root.glob("**/*.struct.yml"))

    errors: list[str] = []
    errors.extend(validate_skill_files(root))
    errors.extend(validate_yaml_parse(struct_files))
    errors.extend(validate_with_structkit(struct_files))
    errors.extend(scan_for_sensitive_placeholders(root))

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    skill_count = len(list(root.glob("**/SKILL.md")))
    print(f"Validation passed: {len(struct_files)} StructKit template(s), {skill_count} skill file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
