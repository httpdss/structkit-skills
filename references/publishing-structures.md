# Publishing StructKit-backed skills and structures

Use a repository layout that humans and agents can both consume.

## Single-skill repository

For skills.sh-style installers, a root-level `SKILL.md` is the most portable layout:

```text
repo/
  SKILL.md
  references/
  templates/
  scripts/
  README.md
```

This repository uses that layout.

## Multi-skill repository

If the repository later grows multiple independent skills, move to a folder-per-skill layout:

```text
repo/
  skills/
    structkit-workflows/
      SKILL.md
      references/
      templates/
      scripts/
    structkit-authoring/
      SKILL.md
      references/
```

Only split when the trigger conditions are truly different; otherwise keep one umbrella skill with support files.

## Release checklist

- [ ] README has install commands.
- [ ] `SKILL.md` version is updated.
- [ ] Validation workflow passes.
- [ ] Templates validate with StructKit.
- [ ] Examples do not contain secrets.
- [ ] Tags/releases describe behavior changes.
