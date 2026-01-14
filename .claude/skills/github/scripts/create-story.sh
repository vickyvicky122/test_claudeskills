#!/bin/bash
# Create a story with auto-incrementing ID, linked to an epic
# Usage: create-story.sh <epic-number> "Story Title"

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

# Get epic number from argument or prompt
if [ -n "$1" ]; then
    EPIC_NUM="$1"
    shift
else
    # List available epics
    echo "Available epics:"
    gh issue list --repo "$REPO" --label "epic" --json number,title --jq '.[] | "  #\(.number): \(.title)"'
    echo ""
    read -p "Epic number (e.g., 1 for epic-1): " EPIC_NUM
fi

if [ -z "$EPIC_NUM" ]; then
    echo "Error: Epic number is required"
    exit 1
fi

EPIC_KEY="epic-$EPIC_NUM"

# Verify epic exists
if ! gh label list --repo "$REPO" --json name --jq '.[].name' | grep -q "^${EPIC_KEY}$"; then
    echo "Error: Epic $EPIC_KEY does not exist"
    echo "Create it first with: create-epic.sh \"Epic Title\""
    exit 1
fi

# Get story title from argument or prompt
if [ -n "$1" ]; then
    TITLE="$1"
else
    read -p "Story title: " TITLE
fi

if [ -z "$TITLE" ]; then
    echo "Error: Story title is required"
    exit 1
fi

# Find next story number for this epic
echo "Finding next story number for $EPIC_KEY..."
EXISTING_STORIES=$(gh issue list --repo "$REPO" --label "$EPIC_KEY,story" --json title --jq '.[].title' 2>/dev/null | grep -oE "Story ${EPIC_NUM}\.[0-9]+" | grep -oE '\.[0-9]+' | tr -d '.' | sort -n | tail -1)

if [ -z "$EXISTING_STORIES" ]; then
    NEXT_STORY=1
else
    NEXT_STORY=$((EXISTING_STORIES + 1))
fi

STORY_KEY="epic-$EPIC_NUM-story-$NEXT_STORY"
STORY_ID="$EPIC_NUM.$NEXT_STORY"
STORY_TITLE="Story $STORY_ID: $TITLE"

echo ""
echo "Creating: $STORY_TITLE"
echo "Key: $STORY_KEY"
echo "Epic: $EPIC_KEY"
echo ""

# Create story label if doesn't exist
if ! gh label list --repo "$REPO" --json name --jq '.[].name' | grep -q "^story$"; then
    echo "Creating label: story"
    gh label create "story" --repo "$REPO" --color "0E8A16" --description "User story" 2>/dev/null || true
fi

# Prompt for user story format
echo "Enter description (or press Enter for default format):"
read -p "> " DESCRIPTION

if [ -z "$DESCRIPTION" ]; then
    read -p "As a [user type]: " USER_TYPE
    read -p "I want to [action]: " ACTION
    read -p "So that [benefit]: " BENEFIT

    if [ -n "$USER_TYPE" ] && [ -n "$ACTION" ] && [ -n "$BENEFIT" ]; then
        DESCRIPTION="As a $USER_TYPE, I want to $ACTION so that $BENEFIT."
    else
        DESCRIPTION="$TITLE"
    fi
fi

# Prompt for acceptance criteria
echo ""
echo "Enter acceptance criteria (one per line, empty line to finish):"
AC_LIST=""
AC_NUM=1
while IFS= read -r line; do
    [ -z "$line" ] && break
    AC_LIST="${AC_LIST}- [ ] AC$AC_NUM: $line\n"
    AC_NUM=$((AC_NUM + 1))
done

if [ -z "$AC_LIST" ]; then
    AC_LIST="- [ ] AC1: TBD\n- [ ] AC2: TBD\n- [ ] AC3: TBD"
fi

# Get epic title for reference
EPIC_TITLE=$(gh issue list --repo "$REPO" --label "$EPIC_KEY,epic" --json title --jq '.[0].title // "Epic '"$EPIC_NUM"'"')

# Create the issue body
BODY=$(cat <<EOF
**Story Key:** $STORY_KEY
**Epic:** $EPIC_TITLE
**Status:** Backlog

---

## Description
$DESCRIPTION

## Acceptance Criteria
$(echo -e "$AC_LIST")

## Technical Notes
- TBD

## Out of Scope
- TBD

---
*Part of $EPIC_KEY*
EOF
)

# Create the issue
echo "Creating story issue..."
ISSUE_URL=$(gh issue create --repo "$REPO" \
    --title "$STORY_TITLE" \
    --label "story,$EPIC_KEY" \
    --body "$BODY" \
    --json url --jq '.url')

ISSUE_NUM=$(echo "$ISSUE_URL" | grep -oE '[0-9]+$')

echo ""
echo "Story created: $ISSUE_URL"

# Add to project board
echo "Adding to project board..."
gh project item-add "$PROJECT_NUMBER" --owner "$OWNER" --url "$ISSUE_URL" 2>/dev/null || echo "Note: Could not add to project board automatically"

echo ""
echo "=== Story Created ==="
echo "Title: $STORY_TITLE"
echo "Key: $STORY_KEY"
echo "Epic: $EPIC_KEY"
echo "Issue: #$ISSUE_NUM"
echo "URL: $ISSUE_URL"
echo ""
echo "Branch name suggestion:"
echo "  git checkout -b $ISSUE_NUM-$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-')"
