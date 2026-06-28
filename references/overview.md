# StructKit overview for agents

StructKit turns YAML structure definitions into generated files and folders. It is useful for platform/DevEx templates, Terraform modules, app skeletons, CI baselines, docs bundles, and agent-approved scaffolds.

Agent mental model:

```text
structure definition + variables + output directory + file strategy => generated artifact
```

Before generating, resolve:

- Structure identifier: bundled name, custom structure name, or direct YAML path.
- Structures path: default bundled structures, `STRUCTKIT_STRUCTURES_PATH`, or explicit `--structures-path`.
- Variables: inline `--vars`, mappings files, defaults, or user-provided values.
- File strategy: skip, backup, overwrite, append, rename, etc. depending on tool/CLI support.
- Network posture: allowed or denied for remote `file:` references.

Use StructKit especially when the user wants consistency across multiple repositories or wants an AI agent to scaffold from approved patterns instead of inventing layouts.
