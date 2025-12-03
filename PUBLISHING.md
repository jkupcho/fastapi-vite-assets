# Publishing fastapi-vite-assets to PyPI

This guide explains how to publish the `fastapi-vite-assets` package to PyPI.

## Prerequisites

✅ PyPI trusted publishing is already configured for this repository.

## Publishing Workflow

### Publishing a New Release (Fully Automated) ⚡

The project now has **fully automated releases** via GitHub Actions:

1. **Make conventional commits** as you develop:
   ```bash
   git commit -m "feat: add new feature"
   git commit -m "fix: resolve bug"
   ```

2. **Push to main branch** (via PR or direct push):
   ```bash
   git push origin main
   ```

3. **Automatic Release** 🤖:
   - GitHub Actions detects your `feat`/`fix` commits
   - Automatically bumps version using Commitizen
   - Updates `pyproject.toml` and `CHANGELOG.md`
   - Creates package-prefixed git tag (`fastapi-vite-assets-v0.2.0`)
   - Creates GitHub Release:
     - **Minor/Patch versions**: Published automatically
     - **Major versions**: Created as draft (requires manual approval)
   - Publishes to PyPI via trusted publishing

**That's it!** No manual version bumping or GitHub release creation needed.

### Manual Release Override (Optional)

If you need to manually trigger a release or override the automation:

1. **Run the release script locally**:
   ```bash
   uv run scripts/release.py --commit
   git push
   ```

2. **Create GitHub Release manually**:
   - Go to your repository on GitHub
   - Click "Releases" → "Create a new release"
   - Click "Choose a tag"
   - Type `fastapi-vite-assets-v0.2.0` (package-prefixed) and click "Create new tag"
   - Release title: `fastapi-vite-assets v0.2.0`
   - Description: Add release notes/changelog
   - Click "Publish release"

3. **Automatic Publishing**:
   - GitHub Actions will automatically trigger the `publish.yml` workflow
   - The package will be built and published to PyPI via trusted publishing
   - Monitor progress in the "Actions" tab
   - Verify at [pypi.org/project/fastapi-vite-assets](https://pypi.org/project/fastapi-vite-assets)

## Version Management

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR** version (1.0.0): Incompatible API changes
- **MINOR** version (0.1.0): Add functionality (backwards-compatible)
- **PATCH** version (0.0.1): Bug fixes (backwards-compatible)

## Pre-commit Hooks

The project uses **pre-commit hooks** to ensure code quality before commits:

### Setup (One-time)

```bash
# After cloning the repository, install hooks
uv run pre-commit install
```

### What Gets Checked

Pre-commit automatically runs on every commit:
- **Ruff format**: Auto-formats Python code
- **Ruff lint**: Catches common errors
- **Trailing whitespace**: Removes trailing spaces
- **End-of-file**: Ensures files end with newline
- **YAML/TOML syntax**: Validates configuration files
- **Large files**: Prevents accidentally committing large files

### Manual Usage

```bash
# Run hooks on all files
uv run pre-commit run --all-files

# Run hooks on staged files only
uv run pre-commit run

# Skip hooks for emergency commits (use sparingly)
git commit --no-verify -m "emergency fix"
```

## Pre-release Checklist

Before publishing a new version, ensure all tests pass and the build works:

```bash
# 1. Run all tests
cd packages/fastapi-vite-assets
uv run pytest

# 2. Test in the example app
cd ../example
uv run fastapi dev app/main.py
cd web
npm run dev
# Verify app works correctly in browser

# 3. Build locally to verify
cd ../fastapi-vite-assets
uv build

# 4. Inspect build output
ls -la dist/
# Should see .whl and .tar.gz files

# 5. (Optional) Test wheel installation
pip install dist/fastapi_vite_assets-0.2.0-py3-none-any.whl --force-reinstall
```

Checklist:

- [ ] Pre-commit hooks installed (`uv run pre-commit install`)
- [ ] All tests pass (`pytest`)
- [ ] Example app works correctly
- [ ] Local build succeeds
- [ ] Version number updated in pyproject.toml
- [ ] Changes documented (CHANGELOG.md or release notes)
- [ ] All changes committed and pushed

## Quick Release (Automated Script with Conventional Commits)

The project uses **Conventional Commits** to automatically determine version bumps and generate changelogs.

### Basic Usage

```bash
# Run from project root (auto-detects version from commits)
uv run scripts/release.py

# Preview what would happen without making changes
uv run scripts/release.py --dry-run

# Auto-commit if you're confident
uv run scripts/release.py --commit

# Override version manually if needed
uv run scripts/release.py --version 1.0.0
```

### How It Works

The script:
1. 📊 **Analyzes commits** since last release using Commitizen
2. 📝 **Auto-determines version bump**:
   - `feat:` commits → Minor version bump (0.1.0 → 0.2.0)
   - `fix:` commits → Patch version bump (0.1.0 → 0.1.1)
   - `feat!:` or `BREAKING CHANGE:` → Major version bump (0.1.0 → 1.0.0)
3. 📜 **Generates CHANGELOG.md** automatically from commit messages
4. 🧪 Runs all tests
5. 📦 Builds the package
6. 📋 Stages changes (pyproject.toml + CHANGELOG.md)
7. 💾 Optionally commits (with `--commit` flag)
8. 📋 Shows changelog preview and next steps

**Default behavior**: Changes are staged but not committed, so you can review with `git diff --staged` before committing.

### Conventional Commit Format

When making commits, use this format:

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

**Common types:**
- `feat`: New feature (minor version bump)
- `fix`: Bug fix (patch version bump)
- `docs`: Documentation changes (no version bump)
- `chore`: Maintenance tasks (no version bump)
- `refactor`: Code refactoring (no version bump)
- `test`: Adding tests (no version bump)
- `perf`: Performance improvements (patch version bump)

**Examples:**
```bash
git commit -m "feat(config): add support for custom Vite port"
git commit -m "fix: handle missing manifest file gracefully"
git commit -m "docs: update installation instructions"
git commit -m "feat!: redesign configuration API" # Breaking change = major bump
```

### Interactive Commit Helper

Use Commitizen's interactive prompt for guidance:

```bash
git add .
uv run cz commit
# Follow the interactive prompts
```

## Manual Release Command

If you prefer to do it manually:

```bash
# Set your new version
NEW_VERSION="0.2.0"

# Update version, test, build, and commit
cd packages/fastapi-vite-assets

# Update pyproject.toml version
sed -i '' "s/version = \".*\"/version = \"$NEW_VERSION\"/" pyproject.toml

# Run tests
uv run pytest || { echo "Tests failed!"; exit 1; }

# Build
uv build || { echo "Build failed!"; exit 1; }

# Commit
git add pyproject.toml
git commit -m "chore: bump version to $NEW_VERSION"
git push

echo "✅ Version bumped to $NEW_VERSION"
echo "📋 Next steps:"
echo "   1. Go to https://github.com/jkupcho/fastapi-vite-assets/releases/new"
echo "   2. Create new tag: fastapi-vite-assets-v$NEW_VERSION"
echo "   3. Title: fastapi-vite-assets v$NEW_VERSION"
echo "   4. Add release notes"
echo "   5. Publish release"
echo ""
echo "GitHub Actions will automatically publish to PyPI"
```

## Post-Release Verification

After publishing, verify the release:

```bash
# 1. Check PyPI page
open https://pypi.org/project/fastapi-vite-assets/

# 2. Test installation in a fresh environment
python -m venv /tmp/test-install
source /tmp/test-install/bin/activate
pip install fastapi-vite-assets

# 3. Verify import works
python -c "from fastapi_vite_assets import ViteConfig, setup_vite; print('✅ Installation successful!')"

# 4. Check version
python -c "import fastapi_vite_assets; print(f'Version: {fastapi_vite_assets.__version__}')"

# Clean up
deactivate
rm -rf /tmp/test-install
```

## Troubleshooting

### GitHub Actions Publishing Fails

1. Check the Actions tab for error logs
2. Common issues:
   - **Version already exists on PyPI**: You cannot republish the same version. Bump the version number.
   - **Workflow permissions**: Ensure the workflow has `id-token: write` permission
   - **Environment not found**: Verify the `pypi` environment exists in repository settings

### Build Fails Locally

```bash
# Check pyproject.toml syntax
cd packages/fastapi-vite-assets
uv build --verbose

# Inspect what's included in the wheel
unzip -l dist/*.whl
```

Common issues:

- Missing `py.typed` marker file
- Incorrect `packages` configuration in pyproject.toml
- Missing module files

### Version Check

Verify the version is correct:

```bash
# Check pyproject.toml version
grep 'version =' packages/fastapi-vite-assets/pyproject.toml

# Verify __version__ reads from pyproject.toml correctly
cd packages/fastapi-vite-assets
uv run python -c "import fastapi_vite_assets; print(fastapi_vite_assets.__version__)"
```

## Resources

- [PyPI Project Page](https://pypi.org/project/fastapi-vite-assets/)
- [GitHub Actions Workflows](.github/workflows/)
- [Trusted Publishing Documentation](https://docs.pypi.org/trusted-publishers/)
- [Semantic Versioning](https://semver.org/)
