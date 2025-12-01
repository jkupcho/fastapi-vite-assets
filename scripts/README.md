# Project Scripts

This directory contains automation scripts for the project.

## Available Scripts

### `release.py` - Automated Release Process

Automates the process of releasing a new version of `fastapi-vite-assets` to PyPI.

**Usage:**

```bash
# Stage changes only (default - recommended)
uv run scripts/release.py 0.2.0

# Stage and commit changes
uv run scripts/release.py 0.2.0 --commit
```

**What it does:**

1. ✅ Validates version format (MAJOR.MINOR.PATCH)
2. 📝 Updates version in `pyproject.toml`
3. 🧪 Runs all tests (`pytest`)
4. 📦 Builds the package (`uv build`)
5. 📋 Stages the version change
6. 💾 Optionally commits (with `--commit` flag)

**Features:**

- **Safe default**: Stages changes but doesn't commit, giving you a chance to review
- **Validation**: Ensures version follows semantic versioning
- **Rollback**: Automatically reverts changes if tests or build fail
- **Clear output**: Step-by-step status messages for each operation
- **Flexible**: Use `--commit` flag when you're confident

**Requirements:**

- Python 3.10+
- `uv` package manager
- Git repository with write access

**After running:**

The script will guide you to create a GitHub release, which will trigger automatic publishing to PyPI via GitHub Actions.

## How Scripts Work

These scripts use `uv`'s inline script metadata (PEP 723) to declare dependencies. The `# /// script` block at the top of each file tells `uv` what dependencies to install before running the script.

Example:

```python
#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "toml>=0.10.2",
# ]
# ///
```

When you run `uv run scripts/release.py`, `uv` will:
1. Create an isolated environment
2. Install the specified dependencies
3. Run the script

No need to manually manage virtual environments or install dependencies!
