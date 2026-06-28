---
name: structkit-workflows
description: Use StructKit to inspect, preview, generate, validate, and author project structures safely.
version: 0.1.0
author: httpdss
license: MIT
metadata:
  hermes:
    tags:
      - structkit
      - scaffolding
      - code-generation
      - templates
      - project-structure
      - mcp
    homepage: https://github.com/httpdss/structkit-skills
    related_skills: []
---

# StructKit Workflows

Use this skill when the user wants to use [StructKit](https://github.com/httpdss/structkit) to inspect structures, preview generated files, scaffold projects, validate `.struct.yaml` files, author reusable structures, or package StructKit-backed workflows for agents.

StructKit is a YAML-first scaffolding tool. The agent's job is to make generation predictable: inspect first, preview before writing, preserve user files, and verify the result.

## Default principles

- **Inspect before generate** — identify the structure, variables, output path, custom `structures_path`, and file strategy before writing.
- **Preview before write** — use dry-run/diff previews by default. Do not skip previews for non-trivial generation.
- **Protect existing files** — prefer `skip`, `backup`, or explicit overwrite strategy. Do not overwrite user work unless the user clearly requested it.
- **Validate after changes** — validate structure definitions and run project-appropriate checks for generated code/config.
- **Keep structures reusable** — use variables, templates, nested structures, and references instead of hardcoded one-off content.
- **Keep network explicit** — if generation may fetch remote content, tell the user. For locked-down/offline runs, set or request `STRUCTKIT_DENY_NETWORK=1` where supported.

## Preferred tool order

When StructKit tools are available in the agent environment, prefer them over shelling out:

1. `structkit_list` — discover available structures.
2. `structkit_info` — inspect a selected structure.
3. `structkit_vars` — inspect required/default variables.
4. `structkit_preview` — dry-run/diff generation.
5. `structkit_generate` — write files only after preview/scope is acceptable.
6. `structkit_validate` — validate `.struct.yaml` definitions.

Use the `structkit` CLI as a fallback when dedicated tools are unavailable.

## Standard generation workflow

1. **Resolve source**
   - Structure name or local `.struct.yaml` path.
   - Optional custom structures directory via `--structures-path` or `STRUCTKIT_STRUCTURES_PATH`.
   - Optional mappings file(s).

2. **Inspect**
   - List structures if the requested structure name is ambiguous.
   - Inspect structure metadata and variables.
   - Collect missing variables from the user only when they cannot be inferred safely.

3. **Preview**
   - Run a dry-run/diff preview against the exact output directory.
   - Use a conservative file strategy (`skip` or `backup`) unless overwrite is explicitly desired.
   - For remote file references, note whether network is required.

4. **Generate**
   - Generate only after output path and conflict behavior are clear.
   - Do not write outside the active workspace unless the user explicitly approves the absolute path.

5. **Verify**
   - Run `structkit validate` for changed `.struct.yaml` files.
   - Check generated files exist and expected variables rendered.
   - Run repo-specific tests/linters/builds when generated output affects executable code.

See [`references/safe-generation.md`](references/safe-generation.md) for the full safety checklist.

## Authoring structures

When creating or modifying a StructKit structure:

- Include a short description and examples in the surrounding README/docs.
- Declare variables with descriptions, types, and defaults where reasonable.
- Use `skip_if_exists` for user-editable files that should not be replaced after first generation.
- Use `permissions` for scripts and sensitive files.
- Compose nested structures instead of duplicating large blocks.
- Validate the YAML and, when possible, preview it in a temporary directory.

See [`references/authoring-structures.md`](references/authoring-structures.md).

## CLI fallback patterns

```bash
# Discover
structkit list
structkit info <structure> --structures-path ./structures
structkit vars <structure> --structures-path ./structures

# Validate
structkit validate ./structures/my-structure.struct.yaml

# Preview / dry-run before writing
structkit generate <structure> ./out --dry-run --diff --vars name=value

# Generate with conservative file handling
structkit generate <structure> ./out --backup --file-strategy skip --vars name=value
```

If CLI flags differ by StructKit version, run `structkit <command> --help` and adapt while preserving the workflow: inspect → preview → generate → validate.

## Common pitfalls

- **Accidental overwrites** — always preview and choose conflict behavior before writing.
- **Wrong structure source** — distinguish bundled structures from a custom `structures_path` or direct `.struct.yaml` file.
- **Missing variables** — run variable inspection before generation; do not invent secrets or organization-specific values.
- **Remote fetch surprises** — remote `file:` sources can require HTTP, GitHub, SSH, or cloud credentials.
- **Generated secrets** — never commit real secrets into generated structures or examples.
- **One-off structures** — if the same pattern may be reused, extract variables and references rather than baking in a single project name.

## Verification checklist

- [ ] Target output directory is correct.
- [ ] Structure source and version/path are known.
- [ ] Required variables are supplied or defaults are acceptable.
- [ ] Preview/diff was reviewed.
- [ ] File conflict strategy is explicit.
- [ ] `.struct.yaml` files validate.
- [ ] Generated output was inspected or tested.
- [ ] No secrets or machine-local paths were introduced.
