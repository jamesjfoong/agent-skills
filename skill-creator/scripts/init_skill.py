#!/usr/bin/env python3
"""Create a portable Agent Skill directory from a template.

Usage:
    python scripts/init_skill.py my-skill --path path/to/skills
    python scripts/init_skill.py my-skill --path path/to/skills --minimal
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

MAX_SKILL_NAME_LENGTH = 64

SKILL_TEMPLATE = """---
name: {skill_name}
description: [TODO: Explain what this skill does and when to use it. Include specific task types, file types, user phrases, and contexts that should trigger it.]
---

# {skill_title}

## Overview

[TODO: Explain in 1-2 sentences what this skill enables an agent to do.]

## Workflow

[TODO: Add the core workflow. Use clear steps, decision points, and links to resources when needed.]

## Resources

[TODO: Reference only the resources this skill actually includes.]

- `scripts/`: Executable helpers for deterministic or repeated work.
- `references/`: Detailed knowledge the agent should read only when needed.
- `assets/`: Templates, starter files, or media used in final outputs.
"""

EXAMPLE_SCRIPT = '''#!/usr/bin/env python3
"""Example helper script for {skill_name}.

Replace this file with real deterministic logic, or delete it if this skill
does not need scripts.
"""


def main() -> None:
    print("Example helper for {skill_name}")


if __name__ == "__main__":
    main()
'''

EXAMPLE_REFERENCE = """# Reference Notes For {skill_title}

Replace this file with domain knowledge, API details, examples, schemas, or
long-form workflow guidance that does not need to live in SKILL.md.

## When To Read

Read this reference when [TODO: describe the specific situation].
"""

EXAMPLE_ASSET = """This is an example asset placeholder.

Replace it with templates, starter files, images, fonts, or sample data that
the skill should use in outputs. Delete this file if the skill does not need
assets.
"""


def validate_name(name: str) -> tuple[bool, str]:
    """Validate portable skill names."""
    if not name or not name.strip():
        return False, "cannot be empty"
    if len(name) > MAX_SKILL_NAME_LENGTH:
        return False, "cannot exceed 64 characters"
    if name.startswith("-") or name.endswith("-") or "--" in name:
        return False, "cannot start/end with hyphen or contain consecutive hyphens"
    for char in name:
        if char == "-":
            continue
        if (char.isalpha() and char.islower()) or char.isdigit():
            continue
        return False, "must contain only lowercase letters, digits, and hyphens"
    return True, ""


def title_case_skill_name(skill_name: str) -> str:
    """Convert a hyphenated skill name to a display title."""
    return " ".join(part.capitalize() for part in skill_name.split("-"))


def write_text(path: Path, content: str, executable: bool = False) -> None:
    """Write a UTF-8 text file and optionally mark it executable."""
    path.write_text(content, encoding="utf-8")
    if executable:
        path.chmod(0o755)


def init_skill(skill_name: str, output_path: Path, minimal: bool = False) -> Path:
    """Create the skill directory and starter files."""
    is_valid, error = validate_name(skill_name)
    if not is_valid:
        raise ValueError(f"invalid skill name: {error}")

    skill_dir = output_path.expanduser().resolve() / skill_name
    if skill_dir.exists():
        raise FileExistsError(f"skill directory already exists: {skill_dir}")

    skill_title = title_case_skill_name(skill_name)
    try:
        skill_dir.mkdir(parents=True)
        write_text(
            skill_dir / "SKILL.md",
            SKILL_TEMPLATE.format(skill_name=skill_name, skill_title=skill_title),
        )

        if not minimal:
            scripts_dir = skill_dir / "scripts"
            references_dir = skill_dir / "references"
            assets_dir = skill_dir / "assets"

            scripts_dir.mkdir()
            references_dir.mkdir()
            assets_dir.mkdir()

            write_text(
                scripts_dir / "example.py",
                EXAMPLE_SCRIPT.format(skill_name=skill_name),
                executable=True,
            )
            write_text(
                references_dir / "notes.md",
                EXAMPLE_REFERENCE.format(skill_title=skill_title),
            )
            write_text(assets_dir / "example_asset.txt", EXAMPLE_ASSET)
    except Exception:
        shutil.rmtree(skill_dir, ignore_errors=True)
        raise

    return skill_dir


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_name", help="Skill name, such as data-cleaner")
    parser.add_argument(
        "--path",
        required=True,
        type=Path,
        help="Directory where the skill folder should be created",
    )
    parser.add_argument(
        "--minimal",
        action="store_true",
        help="Create only SKILL.md without example resource directories",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        skill_dir = init_skill(args.skill_name, args.path, minimal=args.minimal)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Created skill: {skill_dir}")
    print("Next steps:")
    print("1. Complete SKILL.md and its description.")
    print("2. Replace or delete placeholder resources.")
    print("3. Run scripts/quick_validate.py on the skill directory.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
