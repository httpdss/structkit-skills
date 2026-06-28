# Safe generation checklist

Use this checklist before any StructKit operation that writes files.

## 1. Confirm scope

- Output directory is the intended workspace or a new subdirectory.
- The user explicitly requested any absolute path outside the current workspace.
- Existing files in the output directory are known.

## 2. Inspect first

Run the equivalent of:

```bash
structkit info <structure>
structkit vars <structure>
```

If using custom structures:

```bash
structkit info -s ./structures <structure>
structkit vars -s ./structures <structure>
```

## 3. Preview changes

Prefer a dry run with a diff:

```bash
structkit generate <structure> ./target --dry-run --diff --vars key=value
```

If dedicated agent tools exist, use `structkit_preview`.

## 4. Choose conflict behavior

Recommended defaults:

- New project directory: normal generation is usually safe.
- Existing repo: use skip/backup unless the user asks for overwrite.
- User-editable generated files: prefer `skip_if_exists` inside the structure.
- Destructive overwrite: only after explicit confirmation.

## 5. Generate

Use the exact values from the preview. Do not silently change variables, mappings files, output path, or structures path between preview and generation.

## 6. Verify

- Validate changed `.struct.yaml` files.
- Inspect `git diff --check` when inside a Git repo.
- Run relevant tests/lints/builds for generated code.
- Report generated paths and real verification output.
