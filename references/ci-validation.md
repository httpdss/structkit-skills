# CI validation for StructKit skill and structure repos

A StructKit skill/template repository should catch broken YAML and broken examples before users install it.

Minimum checks:

1. Verify every `SKILL.md` has frontmatter with `name`, `description`, and `version`.
2. Verify every `*.struct.yaml` / `*.struct.yml` parses as YAML.
3. Run `structkit validate` for every template structure when StructKit is installed.
4. Scan examples for obvious placeholder secrets.

Suggested GitHub Actions workflow:

```yaml
name: Validate
on:
  push:
    branches: [main]
  pull_request:

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: python -m pip install --upgrade pip
      - run: python -m pip install structkit pyyaml
      - run: python scripts/validate_structkit_repo.py .
```

For generated-code structures, add a fixture generation job that runs the structure into a temporary directory and executes the generated project's own checks.
