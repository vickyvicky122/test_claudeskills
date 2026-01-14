#!/bin/bash
# Install linting workflow and configuration
# Run from your project root: ~/.claude/skills/github/scripts/install-lint.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== Lint Workflow Installation ==="
echo ""

# Check we're in a git repo
if [ ! -d ".git" ]; then
    echo "Error: Not in a git repository root"
    exit 1
fi

# Install GitHub Actions workflow
echo "Installing .github/workflows/lint.yml..."
mkdir -p .github/workflows
cp "$SKILL_DIR/assets/workflows/lint.yml" ".github/workflows/"
echo "  Installed: .github/workflows/lint.yml"

# Install validation script
echo "Installing scripts/validate_skill.py..."
mkdir -p scripts
cp "$SKILL_DIR/scripts/validate_skill.py" "scripts/"
chmod +x scripts/validate_skill.py
echo "  Installed: scripts/validate_skill.py"

# Install configurations
echo "Installing linter configurations..."
cp "$SKILL_DIR/pyproject.toml" "./" 2>/dev/null || echo "  Skipped: pyproject.toml (already exists)"
cp "$SKILL_DIR/.markdownlint.json" "./" 2>/dev/null || echo "  Skipped: .markdownlint.json (already exists)"
echo "  Installed: pyproject.toml"
echo "  Installed: .markdownlint.json"

echo ""
echo "=== Installation Complete ==="
echo ""
echo "Linting includes:"
echo "  - Skill structure validation (SKILL.md, frontmatter)"
echo "  - Python linting (ruff)"
echo "  - Markdown linting (markdownlint)"
echo "  - Shell script linting (shellcheck)"
echo ""
echo "Run locally:"
echo "  python scripts/validate_skill.py .claude/skills/your-skill"
echo "  pip install ruff && ruff check ."
echo ""
echo "Commit to enable:"
echo "  git add .github scripts pyproject.toml .markdownlint.json"
echo "  git commit -m 'Add linting workflow'"
echo "  git push"
echo ""
