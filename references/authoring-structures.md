# Authoring StructKit structures

Good StructKit structures are small, composable, and safe to re-run.

## Recommended structure pattern

```yaml
variables:
  - project_name:
      description: Human-readable project name.
      type: string
      default: example-project

folders:
  - src: {}

files:
  - README.md:
      skip_if_exists: true
      content: |
        # {{@ project_name @}}

        Generated with StructKit.
```

## Guidelines

- Put variables at the top and document them clearly.
- Prefer defaults for non-sensitive values.
- Never put real credentials in templates.
- Use `skip_if_exists` for files the user will edit after generation.
- Use `permissions: '0755'` for generated scripts.
- Use nested structures for reusable pieces instead of copy-pasting large YAML blocks.
- Include a README/example showing a realistic `structkit generate` command.

## Validation workflow

```bash
structkit validate ./structures/my-structure.struct.yaml
structkit generate ./structures/my-structure.struct.yaml /tmp/structkit-preview --dry-run --diff --vars project_name=demo
```

If the structure references remote files, test both normal network behavior and offline behavior where possible.
