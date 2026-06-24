#!/usr/bin/env python3
"""Validate portable Agent Skill structure and frontmatter."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

import yaml

ALLOWED_PROPERTIES = {
    "name",
    "description",
    "license",
    "compatibility",
    "allowed-tools",
    "metadata",
}

MAX_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
MAX_COMPATIBILITY_LENGTH = 500
RECOMMENDED_MAX_SKILL_MD_LINES = 500


def validate_name(name: str) -> tuple[bool, str]:
    """Validate a portable skill name."""
    if not name or not name.strip():
        return False, "name cannot be empty"
    if len(name) > MAX_NAME_LENGTH:
        return False, f"name exceeds {MAX_NAME_LENGTH} characters"
    if name.startswith("-") or name.endswith("-") or "--" in name:
        return False, "name cannot start/end with hyphen or contain consecutive hyphens"
    for char in name:
        if char == "-":
            continue
        if (char.isalpha() and char.islower()) or char.isdigit():
            continue
        return False, "name must contain only lowercase letters, digits, and hyphens"
    return True, ""


def parse_frontmatter(content: str) -> tuple[dict[str, Any] | None, str | None]:
    """Extract and parse YAML frontmatter from SKILL.md content."""
    if not content.startswith("---"):
        return None, "No YAML frontmatter found"

    match = re.match(r"^---\n(.*?)\n---(?:\n|$)", content, re.DOTALL)
    if not match:
        return None, "Invalid frontmatter format"

    try:
        frontmatter = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        return None, f"Invalid YAML in frontmatter: {exc}"

    if not isinstance(frontmatter, dict):
        return None, "Frontmatter must be a YAML mapping"

    return frontmatter, None


def validate_skill(skill_path: str | Path) -> tuple[bool, str]:
    """Validate a skill directory.

    Returns:
        A tuple of (is_valid, message). Warnings are included in the message
        but do not make the skill invalid.
    """
    skill_dir = Path(skill_path).expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []

    if not skill_dir.exists():
        return False, f"Skill directory not found: {skill_dir}"
    if not skill_dir.is_dir():
        return False, f"Path is not a directory: {skill_dir}"

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md not found"

    content = skill_md.read_text(encoding="utf-8")
    frontmatter, parse_error = parse_frontmatter(content)
    if parse_error:
        return False, parse_error
    assert frontmatter is not None

    unexpected = set(frontmatter) - ALLOWED_PROPERTIES
    if unexpected:
        allowed = ", ".join(sorted(ALLOWED_PROPERTIES))
        errors.append(
            "Unexpected frontmatter key(s): "
            f"{', '.join(sorted(unexpected))}. Allowed keys: {allowed}"
        )

    for required in ("name", "description"):
        if required not in frontmatter:
            errors.append(f"Missing required frontmatter key: {required}")

    name = frontmatter.get("name")
    if name is not None:
        if not isinstance(name, str):
            errors.append(f"name must be a string, got {type(name).__name__}")
        else:
            is_valid, message = validate_name(name.strip())
            if not is_valid:
                errors.append(message)
            elif name.strip() != skill_dir.name:
                warnings.append(
                    f"name '{name.strip()}' does not match directory '{skill_dir.name}'"
                )

    description = frontmatter.get("description")
    if description is not None:
        if not isinstance(description, str):
            errors.append(
                f"description must be a string, got {type(description).__name__}"
            )
        else:
            stripped = description.strip()
            if not stripped:
                errors.append("description cannot be empty")
            if "[TODO" in stripped or "TODO:" in stripped:
                errors.append("description still contains TODO placeholder text")
            if "<" in stripped or ">" in stripped:
                errors.append("description cannot contain angle brackets")
            if len(stripped) > MAX_DESCRIPTION_LENGTH:
                errors.append(
                    "description is too long "
                    f"({len(stripped)} characters, max {MAX_DESCRIPTION_LENGTH})"
                )

    compatibility = frontmatter.get("compatibility")
    if compatibility is not None:
        if not isinstance(compatibility, str):
            errors.append(
                f"compatibility must be a string, got {type(compatibility).__name__}"
            )
        elif len(compatibility.strip()) > MAX_COMPATIBILITY_LENGTH:
            errors.append(
                "compatibility is too long "
                f"({len(compatibility.strip())} characters, "
                f"max {MAX_COMPATIBILITY_LENGTH})"
            )

    body_lines = content.splitlines()
    if len(body_lines) > RECOMMENDED_MAX_SKILL_MD_LINES:
        warnings.append(
            "SKILL.md is long "
            f"({len(body_lines)} lines, recommended max "
            f"{RECOMMENDED_MAX_SKILL_MD_LINES}); consider references/"
        )

    for resource_dir in ("scripts", "references", "assets"):
        path = skill_dir / resource_dir
        if path.exists() and not path.is_dir():
            errors.append(f"{resource_dir} exists but is not a directory")

    sections: list[str] = []
    if errors:
        sections.append("Errors:\n" + "\n".join(f"- {error}" for error in errors))
    if warnings:
        sections.append(
            "Warnings:\n" + "\n".join(f"- {warning}" for warning in warnings)
        )
    if not sections:
        sections.append("Skill is valid.")

    return not errors, "\n\n".join(sections)


def main(argv: list[str] | None = None) -> int:
    args = argv or sys.argv[1:]
    if len(args) != 1:
        print("Usage: python scripts/quick_validate.py path/to/skill", file=sys.stderr)
        return 2

    is_valid, message = validate_skill(args[0])
    print(message)
    return 0 if is_valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
