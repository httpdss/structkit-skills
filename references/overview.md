# StructKit overview for agents

StructKit turns YAML structure definitions into generated files and folders. It is useful for platform/DevEx templates, Terraform modules, app skeletons, CI baselines, docs bundles, and agent-approved scaffolds.

Agent mental model:

```text
structure definition + variables + output directory + file strategy => generated artifact
```

The default project file is `.structkit.yaml` (`structkit init` creates it; `structkit generate` prefers it and still reads legacy `.struct.yaml`).

Before generating, resolve:

- Structure identifier: bundled name, custom structure name, or direct YAML path (`.structkit.yaml` by default).
- Structures path: default bundled structures, `STRUCTKIT_STRUCTURES_PATH`, or explicit `--structures-path`.
- Variables: inline `--vars`, mappings files, defaults, or user-provided values.
- File strategy: skip, backup, overwrite, append, rename, etc. depending on tool/CLI support.
- Hook posture: skipped (`--no-hooks`, `STRUCTKIT_NO_HOOKS`, MCP `no_hooks`) or constrained (`.struct-hooks-allowlist`).
- Network posture: allowed or denied for remote `file:` references.

Use `structkit config print` to inspect the merged configuration when project, user, and CLI layers may disagree.

Use StructKit especially when the user wants consistency across multiple repositories or wants an AI agent to scaffold from approved patterns instead of inventing layouts.
