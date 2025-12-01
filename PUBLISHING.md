# Publishing fastapi-vite-assets to PyPI

This guide explains how to publish the `fastapi-vite-assets` package to PyPI.

## Prerequisites

✅ PyPI trusted publishing is already configured for this repository.

## Publishing Workflow

### Publishing a New Release

1. **Run Pre-release Checklist** (see below)

2. **Update Version Number**:

   ```bash
   # Edit packages/fastapi-vite-assets/pyproject.toml
   # Change version = "0.1.0" to your new version (e.g., "0.2.0")

   # Note: __version__ in __init__.py automatically reads from pyproject.toml
   ```

3. **Update Changelog** (if you have one):

   ```bash
   # Document changes in CHANGELOG.md
   ```

4. **Commit and Push**:

   ```bash
   git add packages/fastapi-vite-assets/pyproject.toml
   git commit -m "chore: bump version to 0.2.0"
   git push
   ```

5. **Create GitHub Release**:

   - Go to your repository on GitHub
   - Click "Releases" → "Create a new release"
   - Click "Choose a tag"
   - Type `v0.2.0` (must start with `v`) and click "Create new tag"
   - Release title: `v0.2.0`
   - Description: Add release notes/changelog
   - Click "Publish release"

6. **Automatic Publishing**:
   - GitHub Actions will automatically trigger the `publish.yml` workflow
   - The package will be built and published to PyPI via trusted publishing
   - Monitor progress in the "Actions" tab
   - Verify at [pypi.org/project/fastapi-vite-assets](https://pypi.org/project/fastapi-vite-assets)

## Version Management

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR** version (1.0.0): Incompatible API changes
- **MINOR** version (0.1.0): Add functionality (backwards-compatible)
- **PATCH** version (0.0.1): Bug fixes (backwards-compatible)

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

- [ ] All tests pass (`pytest`)
- [ ] Example app works correctly
- [ ] Local build succeeds
- [ ] Version number updated in pyproject.toml
- [ ] Changes documented (CHANGELOG.md or release notes)
- [ ] All changes committed and pushed

## Quick Release (Automated Script)

Use the automated release script:

```bash
# Run from project root (recommended - stages changes only)
uv run scripts/release.py 0.2.0

# Or commit automatically if you're confident
uv run scripts/release.py 0.2.0 --commit
```

The script will:
1. ✅ Update version in `pyproject.toml`
2. 🧪 Run all tests
3. 📦 Build the package
4. 📋 Stage changes for review
5. 💾 Optionally commit (with `--commit` flag)
6. 📋 Display next steps

**Default behavior**: Changes are staged but not committed, so you can review with `git diff --staged` before committing.

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
echo "   2. Create new tag: v$NEW_VERSION"
echo "   3. Title: v$NEW_VERSION"
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
