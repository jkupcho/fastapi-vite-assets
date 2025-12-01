#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "toml>=0.10.2",
# ]
# ///
"""Release automation script for fastapi-vite-assets.

Usage:
    uv run scripts/release.py 0.2.0           # Stage changes only
    uv run scripts/release.py 0.2.0 --commit  # Stage and commit changes
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], cwd: Path | None = None) -> tuple[int, str]:
    """Run a command and return exit code and output."""
    result = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout + result.stderr


def main():
    parser = argparse.ArgumentParser(
        description="Prepare a new release of fastapi-vite-assets"
    )
    parser.add_argument("version", help="Version to release (e.g., 0.2.0)")
    parser.add_argument(
        "--commit",
        action="store_true",
        help="Commit the changes after staging (default: stage only)",
    )
    args = parser.parse_args()

    new_version = args.version

    # Validate version format (basic semver check)
    if not re.match(r"^\d+\.\d+\.\d+$", new_version):
        print(f"❌ Invalid version format: {new_version}")
        print("   Version must be in format: MAJOR.MINOR.PATCH (e.g., 0.2.0)")
        sys.exit(1)

    # Find paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    package_dir = project_root / "packages" / "fastapi-vite-assets"
    pyproject_path = package_dir / "pyproject.toml"

    if not pyproject_path.exists():
        print(f"❌ Could not find pyproject.toml at {pyproject_path}")
        sys.exit(1)

    print(f"🚀 Starting release process for version {new_version}")
    print()

    # Step 1: Update version in pyproject.toml
    print("📝 Step 1: Updating version in pyproject.toml...")
    content = pyproject_path.read_text()
    updated_content = re.sub(
        r'version = "[^"]+"',
        f'version = "{new_version}"',
        content,
    )
    pyproject_path.write_text(updated_content)
    print(f"   ✅ Updated version to {new_version}")
    print()

    # Step 2: Run tests
    print("🧪 Step 2: Running tests...")
    exit_code, output = run_command(["uv", "run", "pytest"], cwd=package_dir)
    if exit_code != 0:
        print("   ❌ Tests failed!")
        print(output)
        # Revert changes
        pyproject_path.write_text(content)
        print("   ⏪ Reverted version change")
        sys.exit(1)
    print("   ✅ All tests passed")
    print()

    # Step 3: Build package
    print("📦 Step 3: Building package...")
    exit_code, output = run_command(["uv", "build"], cwd=package_dir)
    if exit_code != 0:
        print("   ❌ Build failed!")
        print(output)
        # Revert changes
        pyproject_path.write_text(content)
        print("   ⏪ Reverted version change")
        sys.exit(1)
    print("   ✅ Build successful")
    print()

    # Step 4: Stage changes
    print("📋 Step 4: Staging changes...")
    relative_path = pyproject_path.relative_to(project_root)
    exit_code, _ = run_command(
        ["git", "add", str(relative_path)],
        cwd=project_root,
    )
    if exit_code != 0:
        print("   ❌ Git add failed!")
        sys.exit(1)
    print(f"   ✅ Staged: {relative_path}")
    print()

    # Step 5: Optionally commit changes
    if args.commit:
        print("💾 Step 5: Committing changes...")
        commit_message = f"chore: bump version to {new_version}"
        exit_code, _ = run_command(
            ["git", "commit", "-m", commit_message],
            cwd=project_root,
        )
        if exit_code != 0:
            print("   ❌ Git commit failed!")
            sys.exit(1)
        print(f"   ✅ Committed: {commit_message}")
        print()
    else:
        print("💾 Step 5: Skipping commit (changes are staged)")
        print("   Run with --commit to commit automatically")
        print()

    # Print next steps
    print("=" * 60)
    print(f"✅ Version bumped to {new_version}")
    print()

    if not args.commit:
        print("📋 Next steps:")
        print("   1. Review the staged changes: git diff --staged")
        print("   2. Commit the changes: git commit -m 'chore: bump version to {}'".format(new_version))
        print("   3. Push to remote: git push")
        print(f"   4. Create GitHub release: https://github.com/jkupcho/fastapi-vite-assets/releases/new")
        print(f"      - Tag: v{new_version}")
        print(f"      - Title: v{new_version}")
        print("      - Add release notes")
    else:
        print("📋 Next steps:")
        print("   1. Push to remote: git push")
        print(f"   2. Create GitHub release: https://github.com/jkupcho/fastapi-vite-assets/releases/new")
        print(f"      - Tag: v{new_version}")
        print(f"      - Title: v{new_version}")
        print("      - Add release notes")

    print()
    print("🤖 GitHub Actions will automatically publish to PyPI after release")
    print("=" * 60)


if __name__ == "__main__":
    main()
