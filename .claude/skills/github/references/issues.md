# Issue Management

## View Issues

```bash
# List open issues
gh issue list

# Filter by label
gh issue list --label "bug"

# Filter by assignee
gh issue list --assignee @me

# Filter by state
gh issue list --state closed

# View specific issue
gh issue view 123

# View with comments
gh issue view 123 --comments

# Search issues
gh search issues "query" --repo owner/repo
```

## Create Issues

```bash
# Create issue interactively
gh issue create

# Create with parameters
gh issue create --title "Title" --body "Description" --label "bug" --assignee "@me"

# Create from file
gh issue create --title "Title" --body-file issue-body.md

# Create and get URL
gh issue create --title "Title" --body "Body" --json url --jq '.url'
```

## Update Issues

```bash
# Edit issue
gh issue edit 123 --title "New title" --add-label "priority"

# Close issue
gh issue close 123

# Reopen issue
gh issue reopen 123

# Add comment
gh issue comment 123 --body "Comment text"

# Assign user
gh issue edit 123 --add-assignee username

# Remove assignee
gh issue edit 123 --remove-assignee username
```

## Labels

```bash
# List labels
gh label list

# Create label
gh label create "label-name" --color "FF0000" --description "Label description"

# Delete label
gh label delete "label-name"
```
