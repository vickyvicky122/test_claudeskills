#!/bin/bash
# Install board-sync GitHub Actions workflow
# Run from your project root: ~/.claude/skills/github/scripts/install-board-sync.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== Board Sync Workflow Installation ==="
echo ""

# Check we're in a git repo
if [ ! -d ".git" ]; then
    echo "Error: Not in a git repository root"
    exit 1
fi

# Check for config
if [ ! -f "github-config.yaml" ]; then
    echo "Error: No github-config.yaml found"
    echo "Run setup-config.sh first"
    exit 1
fi

# Install GitHub Actions workflow
echo "Installing .github/workflows/board-sync.yml..."
mkdir -p .github/workflows
cp "$SKILL_DIR/assets/workflows/board-sync.yml" ".github/workflows/"
echo "Installed: .github/workflows/board-sync.yml"

echo ""
echo "=== Setup Required ==="
echo ""
echo "Add repository secret for board access:"
echo ""
echo "  1. Go to: https://github.com/settings/tokens?type=beta"
echo "  2. Create token with 'Projects' permission (read/write)"
echo "  3. Add to repo secrets:"
echo "     Settings → Secrets → Actions → New repository secret"
echo "     Name: BOARD_SYNC_TOKEN"
echo "     Value: <your token>"
echo ""
echo "=== Board Sync Flow ==="
echo ""
echo "  ┌─────────────────────────┬──────────────────┐"
echo "  │ GitHub Event            │ Board Action     │"
echo "  ├─────────────────────────┼──────────────────┤"
echo "  │ Branch created (123-*)  │ → In Progress    │"
echo "  │ PR opened (Closes #123) │ → In Review      │"
echo "  │ PR merged               │ → Done           │"
echo "  └─────────────────────────┴──────────────────┘"
echo ""
echo "Commit the workflow file to enable:"
echo "  git add .github/workflows/board-sync.yml"
echo "  git commit -m 'Add board sync workflow'"
echo "  git push"
echo ""
