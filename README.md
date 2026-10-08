# StructKit Skills

Companion to [StructKit](https://github.com/httpdss/structkit). Agent skills so an assistant inspects, previews, generates, and validates from your YAML. Star the [core repo](https://github.com/httpdss/structkit).

- [`structkit-workflows`](./SKILL.md) — inspect, preview, generate, validate, and author StructKit structures.

## Install

### skills.sh / Skills CLI

This repository is laid out as a single root-level skill so Skills-compatible installers can install it directly:

```bash
npx skills add httpdss/structkit-skills
```

If your installer accepts raw `SKILL.md` URLs, use:

```bash
npx skills add https://raw.githubusercontent.com/httpdss/structkit-skills/main/SKILL.md
```

### Hermes Agent

```bash
hermes skills install https://raw.githubusercontent.com/httpdss/structkit-skills/main/SKILL.md --name structkit-workflows
```

Or add the repository as a tap if your Hermes version supports GitHub skill taps:

```bash
hermes skills tap add httpdss/structkit-skills
```

## What this skill optimizes for

- Prefer StructKit-native tools/MCP when available.
- Inspect structures and variables before generation.
- Preview diffs before writing files.
- Avoid overwrites unless explicitly requested.
- Validate `.structkit.yaml` files and generated outputs. Legacy `.struct.yaml` is still read.
- Keep custom structures reusable, composable, and CI-checked.

## Repository layout

```text
.
├── SKILL.md
├── references/
│   ├── overview.md
│   ├── safe-generation.md
│   ├── authoring-structures.md
│   ├── ci-validation.md
│   └── publishing-structures.md
├── templates/
│   ├── basic-structure.struct.yaml
│   └── repo-scaffold.struct.yaml
├── scripts/
│   └── validate_structkit_repo.py
└── .github/workflows/validate.yml
```

## Validate locally

```bash
python scripts/validate_structkit_repo.py .
```

If `structkit` is installed, the validation script also runs `structkit validate` against template structures.

## Versioning

Use semantic-ish versions in `SKILL.md`:

- Patch: wording, examples, or reference corrections.
- Minor: new references/templates or workflow sections.
- Major: behavior-changing agent guidance.
