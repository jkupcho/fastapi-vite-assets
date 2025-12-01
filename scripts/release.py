#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "toml>=0.10.2",
# ]
# ///
"""Release automation script for fastapi-vite-assets with Commitizen.

Usage:
    uv run scripts/release.py                # Auto-detect version, stage changes only
    uv run scripts/release.py --commit       # Auto-detect version, stage and commit
    uv run scripts/release.py --version 1.0.0  # Override version
    uv run scripts/release.py --dry-run      # Preview without making changes
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], cwd: Path | None = None, check: bool = False) -> tuple[int, str]:
    """Run a command and return exit code and output."""
    result = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    if check and result.returncode != 0:
        print(f"Command failed: {' '.join(cmd)}")
        print(result.stdout + result.stderr)
        sys.exit(1)
    return result.returncode, result.stdout + result.stderr


def get_current_version(pyproject_path: Path) -> str:
    """Extract current version from pyproject.toml."""
    content = pyproject_path.read_text()
    match = re.search(r'version = "([^"]+)"', content)
    if match:
        return match.group(1)
    print("❌ Could not find version in pyproject.toml")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Prepare a new release of fastapi-vite-assets"
    )
    parser.add_argument(
        "--version",
        help="Override version (e.g., 1.0.0). If not provided, auto-detects from commits",
    )
    parser.add_argument(
        "--commit",
        action="store_true",
        help="Commit the changes after staging (default: stage only)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without modifying files",
    )
    args = parser.parse_args()

    # Find paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    package_dir = project_root / "packages" / "fastapi-vite-assets"
    pyproject_path = package_dir / "pyproject.toml"
    changelog_path = package_dir / "CHANGELOG.md"

    if not pyproject_path.exists():
        print(f"❌ Could not find pyproject.toml at {pyproject_path}")
        sys.exit(1)

    current_version = get_current_version(pyproject_path)
    print(f"🚀 Starting release process (current version: {current_version})")
    print()

    # Step 1: Determine version bump using Commitizen
    print("📊 Step 1: Analyzing commits to determine version bump...")

    if args.version:
        # Manual version override
        new_version = args.version
        if not re.match(r"^\d+\.\d+\.\d+$", new_version):
            print(f"❌ Invalid version format: {new_version}")
            print("   Version must be in format: MAJOR.MINOR.PATCH (e.g., 0.2.0)")
            sys.exit(1)
        print(f"   ⚠️  Manual override: {current_version} → {new_version}")
    else:
        # Auto-detect version using Commitizen
        if args.dry_run:
            exit_code, output = run_command(
                ["uv", "run", "cz", "bump", "--dry-run"],
                cwd=package_dir,
            )
        else:
            # Just check what version would be bumped
            exit_code, output = run_command(
                ["uv", "run", "cz", "bump", "--dry-run"],
                cwd=package_dir,
            )

        if exit_code != 0:
            print("   ❌ Failed to analyze commits!")
            print(output)
            if "No commits found" in output or "No new commits" in output:
                print("\n💡 Hint: Make some conventional commits first (feat:, fix:, etc.)")
            sys.exit(1)

        # Extract new version from dry-run output
        version_match = re.search(r"(\d+\.\d+\.\d+) → (\d+\.\d+\.\d+)", output)
        if version_match:
            new_version = version_match.group(2)
            print(f"   ✅ Auto-detected: {current_version} → {new_version}")
        else:
            print("   ⚠️  No version bump needed (no feat/fix commits found)")
            print("\n💡 Hint: Use 'feat:' for features or 'fix:' for bug fixes")
            sys.exit(0)

    print()

    if args.dry_run:
        print("🔍 DRY RUN MODE - No changes will be made")
        print(f"   Would bump version from {current_version} → {new_version}")
        print(f"   Would update: {pyproject_path.relative_to(project_root)}")
        print(f"   Would update: {changelog_path.relative_to(project_root)}")
        print()
        sys.exit(0)

    # Step 2: Run Commitizen bump (updates version + changelog)
    print("📝 Step 2: Bumping version and updating changelog...")

    if args.version:
        # Manual version: use cz bump with --increment MANUAL
        # Unfortunately, cz doesn't support setting exact version
        # So we need to update files manually and skip cz bump
        print("   ⚠️  Manual version mode: updating files directly...")

        # Update pyproject.toml
        content = pyproject_path.read_text()
        updated_content = re.sub(
            r'version = "[^"]+"',
            f'version = "{new_version}"',
            content,
        )
        # Also update [tool.commitizen] version
        updated_content = re.sub(
            r'\[tool\.commitizen\]\nname = "cz_conventional_commits"\nversion = "[^"]+"',
            f'[tool.commitizen]\nname = "cz_conventional_commits"\nversion = "{new_version}"',
            updated_content,
        )
        pyproject_path.write_text(updated_content)
        print(f"   ✅ Updated pyproject.toml to {new_version}")

        # Update changelog manually (append entry)
        if changelog_path.exists():
            changelog_content = changelog_path.read_text()
            # Insert new version section after header
            header_end = changelog_content.find("\n## ")
            if header_end > 0:
                new_entry = f"\n## {new_version} (Manual release)\n\n### Changes\n\n- Manual version bump to {new_version}\n"
                updated_changelog = changelog_content[:header_end] + new_entry + changelog_content[header_end:]
                changelog_path.write_text(updated_changelog)
                print(f"   ✅ Updated CHANGELOG.md")
    else:
        # Auto version: use commitizen bump
        exit_code, output = run_command(
            ["uv", "run", "cz", "bump", "--yes"],
            cwd=package_dir,
        )

        if exit_code != 0:
            print("   ❌ Version bump failed!")
            print(output)
            sys.exit(1)

        print(f"   ✅ Bumped version to {new_version}")
        print(f"   ✅ Updated CHANGELOG.md")

    print()

    # Step 3: Run tests
    print("🧪 Step 3: Running tests...")
    exit_code, output = run_command(["uv", "run", "pytest"], cwd=package_dir)
    if exit_code != 0:
        print("   ❌ Tests failed!")
        print(output)
        print("\n⚠️  Version has been updated but tests failed. Please fix and commit manually.")
        sys.exit(1)
    print("   ✅ All tests passed")
    print()

    # Step 4: Build package
    print("📦 Step 4: Building package...")
    exit_code, output = run_command(
        ["uv", "build", "--package", "fastapi-vite-assets"],
        cwd=project_root,
    )
    if exit_code != 0:
        print("   ❌ Build failed!")
        print(output)
        print("\n⚠️  Version has been updated but build failed. Please fix and commit manually.")
        sys.exit(1)
    print("   ✅ Build successful")
    print()

    # Step 5: Stage changes
    print("📋 Step 5: Staging changes...")
    relative_pyproject = pyproject_path.relative_to(project_root)
    relative_changelog = changelog_path.relative_to(project_root)

    exit_code, _ = run_command(
        ["git", "add", str(relative_pyproject), str(relative_changelog)],
        cwd=project_root,
    )
    if exit_code != 0:
        print("   ❌ Git add failed!")
        sys.exit(1)
    print(f"   ✅ Staged: {relative_pyproject}")
    print(f"   ✅ Staged: {relative_changelog}")
    print()

    # Step 6: Optionally commit changes
    if args.commit:
        print("💾 Step 6: Committing changes...")
        commit_message = f"chore(release): version {new_version}"
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
        print("💾 Step 6: Skipping commit (changes are staged)")
        print("   Run with --commit to commit automatically")
        print()

    # Step 7: Show changelog preview
    print("📜 Changelog Preview:")
    print("=" * 60)
    if changelog_path.exists():
        changelog_content = changelog_path.read_text()
        # Show first section of changelog (latest version)
        lines = changelog_content.split("\n")
        in_latest = False
        preview_lines = []
        for line in lines:
            if line.startswith("## ") and new_version in line:
                in_latest = True
            elif line.startswith("## ") and in_latest:
                break
            if in_latest:
                preview_lines.append(line)

        print("\n".join(preview_lines[:20]))  # Show first 20 lines
        if len(preview_lines) > 20:
            print("\n... (truncated)")
    print("=" * 60)
    print()

    # Print next steps
    print("=" * 60)
    print(f"✅ Version bumped to {new_version}")
    print()

    if not args.commit:
        print("📋 Next steps:")
        print("   1. Review the staged changes: git diff --staged")
        print(f"   2. Commit the changes: git commit -m 'chore(release): version {new_version}'")
        print("   3. Push to remote: git push")
        print(f"   4. Create GitHub release: https://github.com/jkupcho/fastapi-vite-assets/releases/new")
        print(f"      - Tag: v{new_version}")
        print(f"      - Title: v{new_version}")
        print("      - Copy changelog content from above")
    else:
        print("📋 Next steps:")
        print("   1. Push to remote: git push")
        print(f"   2. Create GitHub release: https://github.com/jkupcho/fastapi-vite-assets/releases/new")
        print(f"      - Tag: v{new_version}")
        print(f"      - Title: v{new_version}")
        print("      - Copy changelog content from above")

    print()
    print("🤖 GitHub Actions will automatically publish to PyPI after release")
    print("=" * 60)


if __name__ == "__main__":
    main()
