#!/usr/bin/env python3
"""Package a valid skill directory as a .skill zip archive.

Use this only when the target environment accepts .skill archives. Otherwise,
hand off the portable skill directory directly.
"""

from __future__ import annotations

import argparse
import fnmatch
import sys
import zipfile
from pathlib import Path

try:
    from quick_validate import validate_skill
except ImportError:  # pragma: no cover - supports python -m scripts.package_skill
    from scripts.quick_validate import validate_skill

EXCLUDE_DIRS = {"__pycache__", ".git", ".pytest_cache", "node_modules"}
EXCLUDE_FILES = {".DS_Store"}
EXCLUDE_GLOBS = {"*.pyc", "*.pyo", "*.tmp", "*.log"}
ROOT_EXCLUDE_DIRS = {"evals", "test-runs"}


def should_exclude(relative_path: Path) -> bool:
    """Return True when a path should not be included in the archive."""
    parts = relative_path.parts
    if any(part in EXCLUDE_DIRS for part in parts):
        return True
    if len(parts) > 1 and parts[1] in ROOT_EXCLUDE_DIRS:
        return True
    if relative_path.name in EXCLUDE_FILES:
        return True
    return any(fnmatch.fnmatch(relative_path.name, pattern) for pattern in EXCLUDE_GLOBS)


def package_skill(skill_path: str | Path, output_dir: str | Path | None = None) -> Path:
    """Validate and package a skill directory."""
    skill_dir = Path(skill_path).expanduser().resolve()
    if not skill_dir.exists():
        raise FileNotFoundError(f"skill directory not found: {skill_dir}")
    if not skill_dir.is_dir():
        raise NotADirectoryError(f"path is not a directory: {skill_dir}")

    is_valid, message = validate_skill(skill_dir)
    if not is_valid:
        raise ValueError(f"validation failed:\n{message}")

    destination = Path(output_dir).expanduser().resolve() if output_dir else Path.cwd()
    destination.mkdir(parents=True, exist_ok=True)

    archive_path = destination / f"{skill_dir.name}.skill"
    temp_archive_path = destination / f"{skill_dir.name}.skill.tmp"
    try:
        with zipfile.ZipFile(temp_archive_path, "w", zipfile.ZIP_DEFLATED) as archive:
            for file_path in sorted(skill_dir.rglob("*")):
                if not file_path.is_file():
                    continue
                archive_name = file_path.relative_to(skill_dir.parent)
                if should_exclude(archive_name):
                    continue
                archive.write(file_path, archive_name)
        temp_archive_path.replace(archive_path)
    except Exception:
        temp_archive_path.unlink(missing_ok=True)
        raise

    return archive_path


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_path", type=Path, help="Path to the skill directory")
    parser.add_argument(
        "output_dir",
        nargs="?",
        type=Path,
        help="Directory where the .skill archive should be written",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        archive_path = package_skill(args.skill_path, args.output_dir)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Packaged skill: {archive_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
