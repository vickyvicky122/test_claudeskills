#!/bin/bash
# Create an epic with auto-incrementing ID
# Usage: create-epic.sh "Epic Title"

set -e

# Check for config
CONFIG_FILE="github-config.yaml"
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: No github-config.yaml found"
    echo "Run setup-config.sh first"
    exit 1
fi

# Parse config
if command -v yq &> /dev/null; then
    REPO=$(yq -r '.repo' "$CONFIG_FILE")
    OWNER=$(yq -r '.owner' "$CONFIG_FILE")
    PROJECT_NUMBER=$(yq -r '.project_number' "$CONFIG_FILE")
else
    REPO=$(grep 'repo:' "$CONFIG_FILE" | cut -d'"' -f2)
    OWNER=$(grep 'owner:' "$CONFIG_FILE" | cut -d'"' -f2)
    PROJECT_NUMBER=$(grep 'project_number:' "$CONFIG_FILE" | awk '{print $2}')
fi

# Get epic title from argument or prompt
if [ -n "$1" ]; then
    TITLE="$1"
else
    read -p "Epic title: " TITLE
fi

if [ -z "$TITLE" ]; then
    echo "Error: Epic title is required"
    exit 1
fi

# Find next epic number by checking existing epic labels
echo "Finding next epic number..."
EXISTING_EPICS=$(gh label list --repo "$REPO" --json name --jq '.[] | select(.name | startswith("epic-")) | .name' 2>/dev/null | grep -oE '[0-9]+' | sort -n | tail -1)

if [ -z "$EXISTING_EPICS" ]; then
    NEXT_NUM=1
else
    NEXT_NUM=$((EXISTING_EPICS + 1))
fi

EPIC_KEY="epic-$NEXT_NUM"
EPIC_TITLE="Epic $NEXT_NUM: $TITLE"

echo ""
echo "Creating: $EPIC_TITLE"
echo "Key: $EPIC_KEY"
echo ""

# Create label for this epic (if doesn't exist)
if ! gh label list --repo "$REPO" --json name --jq '.[].name' | grep -q "^${EPIC_KEY}$"; then
    echo "Creating label: $EPIC_KEY"
    gh label create "$EPIC_KEY" --repo "$REPO" --color "6f42c1" --description "Epic $NEXT_NUM: $TITLE" 2>/dev/null || true
fi

# Create epic label if doesn't exist
if ! gh label list --repo "$REPO" --json name --jq '.[].name' | grep -q "^epic$"; then
    echo "Creating label: epic"
    gh label create "epic" --repo "$REPO" --color "8B5CF6" --description "Epic issue" 2>/dev/null || true
fi

# Prompt for description
echo "Enter epic description (press Enter twice to finish):"
DESCRIPTION=""
while IFS= read -r line; do
    [ -z "$line" ] && break
    DESCRIPTION="${DESCRIPTION}${line}\n"
done

if [ -z "$DESCRIPTION" ]; then
    DESCRIPTION="This epic tracks the overall progress of $TITLE."
fi

# Create the issue body
BODY=$(cat <<EOF
**Epic Key:** $EPIC_KEY
**Status:** Backlog

---

## Goal
$(echo -e "$DESCRIPTION")

## Scope
- [ ] Define scope item 1
- [ ] Define scope item 2
- [ ] Define scope item 3

## Out of Scope
- TBD

## Stories
| Key | Title | Status |
|-----|-------|--------|
| $EPIC_KEY-story-1 | TBD | Backlog |

## Success Metrics
- TBD

---
*This epic tracks the overall progress of $TITLE.*
EOF
)

# Create the issue
echo "Creating epic issue..."
ISSUE_URL=$(gh issue create --repo "$REPO" \
    --title "$EPIC_TITLE" \
    --label "epic,$EPIC_KEY" \
    --body "$BODY" \
    --json url --jq '.url')

echo ""
echo "Epic created: $ISSUE_URL"

# Add to project board
echo "Adding to project board..."
gh project item-add "$PROJECT_NUMBER" --owner "$OWNER" --url "$ISSUE_URL" 2>/dev/null || echo "Note: Could not add to project board automatically"

echo ""
echo "=== Epic Created ==="
echo "Title: $EPIC_TITLE"
echo "Key: $EPIC_KEY"
echo "URL: $ISSUE_URL"
echo ""
echo "Next: Create stories with"
echo "  create-story.sh $NEXT_NUM \"Story title\""
