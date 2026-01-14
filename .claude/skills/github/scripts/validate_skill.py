#!/usr/bin/env python3
"""
Validate Claude skill structure against agentskills.io specification.

Checks:
- SKILL.md exists with proper YAML frontmatter
- Required fields (name, description) are present
- Name follows kebab-case convention (lowercase, numbers, hyphens)
- Field length limits (name ≤64 chars, description ≤1024 chars)
- Name matches parent directory
- No invalid characters

Usage:
    python validate_skill.py ./skill-folder
    python validate_skill.py .  # current directory
"""

import sys
import re
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)


def validate_skill(skill_path: Path) -> list[str]:
    """Validate a skill directory and return list of errors."""
    errors = []

    # Check SKILL.md exists
    skill_file = skill_path / "SKILL.md"
    if not skill_file.exists():
        errors.append("SKILL.md not found")
        return errors

    # Read and parse SKILL.md
    content = skill_file.read_text()

    # Check for YAML frontmatter
    if not content.startswith("---"):
        errors.append("SKILL.md must start with YAML frontmatter (---)")
        return errors

    # Extract frontmatter
    parts = content.split("---", 2)
    if len(parts) < 3:
        errors.append("Invalid YAML frontmatter format (missing closing ---)")
        return errors

    frontmatter_text = parts[1].strip()

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError as e:
        errors.append(f"Invalid YAML in frontmatter: {e}")
        return errors

    if not isinstance(frontmatter, dict):
        errors.append("Frontmatter must be a YAML mapping")
        return errors

    # Check required fields
    if "name" not in frontmatter:
        errors.append("Missing required field: name")
    else:
        name = frontmatter["name"]

        # Check name format (kebab-case)
        if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", name):
            errors.append(
                f"Name '{name}' must be kebab-case (lowercase letters, numbers, hyphens). "
                "Cannot start/end with hyphen or have consecutive hyphens."
            )

        # Check name length
        if len(name) > 64:
            errors.append(f"Name exceeds 64 characters: {len(name)}")

        # Check name matches directory
        if name != skill_path.name:
            errors.append(
                f"Name '{name}' does not match directory name '{skill_path.name}'"
            )

    if "description" not in frontmatter:
        errors.append("Missing required field: description")
    else:
        desc = frontmatter["description"]

        # Check description length
        if len(desc) > 1024:
            errors.append(f"Description exceeds 1024 characters: {len(desc)}")

        if len(desc) < 10:
            errors.append("Description is too short (should describe what skill does)")

    # Check optional fields format
    if "license" in frontmatter and not isinstance(frontmatter["license"], str):
        errors.append("License must be a string")

    if "compatibility" in frontmatter:
        if not isinstance(frontmatter["compatibility"], str):
            errors.append("Compatibility must be a string")
        elif len(frontmatter["compatibility"]) > 500:
            errors.append("Compatibility exceeds 500 characters")

    if "metadata" in frontmatter:
        if not isinstance(frontmatter["metadata"], dict):
            errors.append("Metadata must be a mapping")

    # Check body content length (recommended <500 lines)
    body = parts[2].strip()
    body_lines = body.count("\n") + 1
    if body_lines > 500:
        errors.append(f"SKILL.md body has {body_lines} lines (recommended: <500)")

    return errors


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_skill.py <skill-folder>")
        sys.exit(1)

    skill_path = Path(sys.argv[1]).resolve()

    if not skill_path.is_dir():
        print(f"Error: {skill_path} is not a directory")
        sys.exit(1)

    print(f"Validating skill: {skill_path.name}")
    print("-" * 40)

    errors = validate_skill(skill_path)

    if errors:
        print("FAILED - Found issues:\n")
        for error in errors:
            print(f"  - {error}")
        print()
        sys.exit(1)
    else:
        print("PASSED - Skill structure is valid")
        sys.exit(0)


if __name__ == "__main__":
    main()
