# Projects (Storyboards/Kanban)

GitHub Projects v2 use GraphQL. These commands manage project boards.

**Note:** Use config values from `.claude/github-config.yaml` for `$OWNER`, `$PROJECT_NUMBER`, `$PROJECT_ID`, `$STATUS_FIELD_ID`, and status option IDs.

## View Projects

```bash
# List org projects
gh project list --owner $OWNER

# List user projects
gh project list --owner @me

# View project details
gh project view $PROJECT_NUMBER --owner $OWNER

# View project items
gh project item-list $PROJECT_NUMBER --owner $OWNER --format json

# View project fields (get field IDs for updates)
gh project field-list $PROJECT_NUMBER --owner $OWNER
```

## Manage Project Items

```bash
# Add issue to project
gh project item-add $PROJECT_NUMBER --owner $OWNER --url https://github.com/$REPO/issues/123

# Add PR to project
gh project item-add $PROJECT_NUMBER --owner $OWNER --url https://github.com/$REPO/pull/456

# Delete item from project
gh project item-delete $PROJECT_NUMBER --owner $OWNER --id ITEM_ID

# Archive item
gh project item-archive $PROJECT_NUMBER --owner $OWNER --id ITEM_ID

# Unarchive item
gh project item-archive $PROJECT_NUMBER --owner $OWNER --id ITEM_ID --undo
```

## Create Draft Items

Draft items are cards directly on the board without a linked issue/PR:

```bash
# Create draft item with title only
gh project item-create $PROJECT_NUMBER --owner $OWNER --title "Story title"

# Create draft item with title and body
gh project item-create $PROJECT_NUMBER --owner $OWNER --title "Story title" --body "Description"
```

For story body templates, see `assets/` directory.

## Update Project Item Fields

Moving items between columns requires field IDs from config:

```bash
# Update item's status (using config values)
gh project item-edit --project-id $PROJECT_ID --id $ITEM_ID \
  --field-id $STATUS_FIELD_ID --single-select-option-id $IN_PROGRESS_OPTION_ID

# Update text field
gh project item-edit --project-id $PROJECT_ID --id $ITEM_ID \
  --field-id $FIELD_ID --text "value"

# Update number field
gh project item-edit --project-id $PROJECT_ID --id $ITEM_ID \
  --field-id $FIELD_ID --number 5

# Update date field
gh project item-edit --project-id $PROJECT_ID --id $ITEM_ID \
  --field-id $FIELD_ID --date "2024-01-15"

# Update iteration field
gh project item-edit --project-id $PROJECT_ID --id $ITEM_ID \
  --field-id $FIELD_ID --iteration-id $ITERATION_ID
```

## Add Issue to Board and Set Fields

Complete workflow using config values:

```bash
# 1. Create the issue and capture URL
ISSUE_URL=$(gh issue create --repo $REPO \
  --title "Story 2.1: Feature name" \
  --label "story,epic-2" \
  --body "Story body here..." \
  --json url --jq '.url')

# 2. Add to project board
gh project item-add $PROJECT_NUMBER --owner $OWNER --url "$ISSUE_URL"

# 3. Get the item ID (for field updates)
ITEM_ID=$(gh project item-list $PROJECT_NUMBER --owner $OWNER --format json | \
  jq -r ".items[] | select(.content.url == \"$ISSUE_URL\") | .id")

# 4. Set status to "Todo" (using config status ID)
gh project item-edit --project-id $PROJECT_ID --id $ITEM_ID \
  --field-id $STATUS_FIELD_ID --single-select-option-id $TODO_OPTION_ID

# 5. Set other fields as needed
gh project item-edit --project-id $PROJECT_ID --id $ITEM_ID \
  --field-id $PRIORITY_FIELD_ID --text "High"
```

## Convert Draft to Issue

```bash
# 1. Get draft item details
gh project item-list $PROJECT_NUMBER --owner $OWNER --format json | \
  jq '.items[] | select(.type == "DRAFT_ISSUE")'

# 2. Create the issue in repo with the draft's content
gh issue create --repo $REPO \
  --title "Story title from draft" \
  --body "Story body from draft" \
  --label "story" \
  --json url --jq '.url'

# 3. Add the new issue to the project
gh project item-add $PROJECT_NUMBER --owner $OWNER --url $ISSUE_URL

# 4. Copy field values from draft to new item
gh project item-edit --project-id $PROJECT_ID --id $NEW_ITEM_ID \
  --field-id $STATUS_FIELD_ID --single-select-option-id $STATUS_OPTION_ID

# 5. Delete the original draft item
gh project item-delete $PROJECT_NUMBER --owner $OWNER --id $DRAFT_ITEM_ID
```

## Bulk Create Stories

```bash
# Create multiple stories from a sprint planning file
cat <<'EOF' | while IFS='|' read -r title body labels; do
  gh issue create --repo $REPO \
    --title "$title" \
    --body "$body" \
    --label "$labels" \
    --json url --jq '.url'
done
Story 2.1: API endpoints|## Description\nCreate REST endpoints|story,epic-2,backend
Story 2.2: Frontend forms|## Description\nBuild React forms|story,epic-2,frontend
Story 2.3: Integration tests|## Description\nEnd-to-end tests|story,epic-2,testing
EOF
```

## Common Workflows

**Get project and field info (to populate config):**
```bash
# List projects to find PROJECT_NUMBER
gh project list --owner $OWNER

# Get project ID (for config: project_id)
gh project view $PROJECT_NUMBER --owner $OWNER --format json --jq '.id'

# Get field IDs and status options (for config)
gh project field-list $PROJECT_NUMBER --owner $OWNER --format json
```

**Move issue to "In Progress" (using config):**
```bash
# 1. Get item ID from project
ITEM_ID=$(gh project item-list $PROJECT_NUMBER --owner $OWNER --format json | \
  jq -r '.items[] | select(.content.number == 123) | .id')

# 2. Update status field using config values
gh project item-edit --project-id $PROJECT_ID --id $ITEM_ID \
  --field-id $STATUS_FIELD_ID --single-select-option-id $IN_PROGRESS_OPTION_ID
```

**Triage workflow:**
```bash
# Find issues not in any project
gh issue list --repo $REPO --label "needs-triage"

# Add to project backlog
gh project item-add $PROJECT_NUMBER --owner $OWNER --url $ISSUE_URL

# Set status to backlog
gh project item-edit --project-id $PROJECT_ID --id $ITEM_ID \
  --field-id $STATUS_FIELD_ID --single-select-option-id $BACKLOG_OPTION_ID
```
