# Project Scripts

This directory contains automation scripts for the project.

## Available Scripts

### `release.py` - Automated Release Process with Conventional Commits

Automates the process of releasing a new version of `fastapi-vite-assets` to PyPI using **Conventional Commits** for automatic version detection and changelog generation.

**Basic Usage:**

```bash
# Auto-detect version from commits, stage changes only (recommended)
uv run scripts/release.py

# Preview what would happen without making changes
uv run scripts/release.py --dry-run

# Auto-detect version and commit automatically
uv run scripts/release.py --commit

# Override version manually if needed
uv run scripts/release.py --version 1.0.0
```

**What it does:**

1. 📊 **Analyzes commits** since last release using Commitizen
2. 📝 **Auto-determines version bump** based on commit types:
   - `feat:` commits → Minor version bump (0.1.0 → 0.2.0)
   - `fix:` commits → Patch version bump (0.1.0 → 0.1.1)
   - `feat!:` or `BREAKING CHANGE:` → Major version bump (0.1.0 → 1.0.0)
3. 📜 **Updates CHANGELOG.md** automatically from commit messages
4. 📝 Updates version in `pyproject.toml`
5. 🧪 Runs all tests (`pytest`)
6. 📦 Builds the package (`uv build`)
7. 📋 Stages changes (pyproject.toml + CHANGELOG.md)
8. 💾 Optionally commits (with `--commit` flag)
9. 📋 Shows changelog preview and next steps

**Features:**

- **Automatic versioning**: No need to manually specify version number
- **Changelog generation**: Automatically generated from conventional commit messages
- **Safe default**: Stages changes but doesn't commit, giving you a chance to review
- **Dry-run mode**: Preview changes without modifying files
- **Manual override**: Can still specify exact version with `--version` flag
- **Clear output**: Step-by-step status messages for each operation
- **Flexible**: Use `--commit` flag when you're confident

**Conventional Commit Format:**

When making commits, use this format for automatic versioning:

```bash
# Features (minor version bump)
git commit -m "feat(config): add custom Vite port support"

# Bug fixes (patch version bump)
git commit -m "fix: handle missing manifest file gracefully"

# Breaking changes (major version bump)
git commit -m "feat!: redesign configuration API"

# Other types (no version bump)
git commit -m "docs: update installation instructions"
git commit -m "chore: update dependencies"
```

**Interactive Commit Helper:**

Use Commitizen's interactive prompt for guidance:

```bash
git add .
uv run cz commit
# Follow the interactive prompts
```

**Requirements:**

- Python 3.10+
- `uv` package manager
- Git repository with write access
- Conventional commit messages for automatic versioning

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
