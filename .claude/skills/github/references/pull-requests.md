# Pull Request Operations

## View Pull Requests

```bash
# List open PRs
gh pr list

# Filter by state
gh pr list --state merged
gh pr list --state closed

# Filter by author
gh pr list --author @me

# Filter by base branch
gh pr list --base main

# View specific PR
gh pr view 123

# View diff
gh pr diff 123

# View PR checks status
gh pr checks 123

# View PR files changed
gh pr view 123 --json files --jq '.files[].path'
```

## Create Pull Requests

```bash
# Create interactively
gh pr create

# Create with parameters
gh pr create --title "PR Title" --body "Description" --base main --head feature-branch

# Create draft
gh pr create --draft --title "WIP: Feature"

# Create and request reviewers
gh pr create --title "Title" --reviewer username1,username2

# Create from body file
gh pr create --title "Title" --body-file pr-body.md

# Create and get URL
gh pr create --title "Title" --body "Body" --json url --jq '.url'
```

## Link PR to Issue (Auto-Close)

Use closing keywords in the PR body to automatically close issues when PR merges:

| Keyword | Example |
|---------|---------|
| `close`, `closes`, `closed` | `Closes #123` |
| `fix`, `fixes`, `fixed` | `Fixes #456` |
| `resolve`, `resolves`, `resolved` | `Resolves #789` |

```bash
# Create PR that closes an issue on merge
gh pr create --title "Add login feature" \
  --body "Implements user authentication.

Closes #42"

# Link multiple issues
gh pr create --title "Fix auth bugs" \
  --body "This PR addresses several issues:

Fixes #10
Fixes #15
Closes #22"

# Cross-repo linking (same org)
gh pr create --title "Update shared lib" \
  --body "Fixes your-org/other-repo#99"
```

**Note:** The issue is closed only when the PR is merged to the default branch (or the branch specified in repo settings).

## Manage Pull Requests

```bash
# Edit PR
gh pr edit 123 --title "New title" --add-label "ready"

# Mark ready for review
gh pr ready 123

# Convert to draft
gh pr ready 123 --undo

# Merge PR (different strategies)
gh pr merge 123 --merge
gh pr merge 123 --squash
gh pr merge 123 --rebase

# Merge and delete branch
gh pr merge 123 --squash --delete-branch

# Close without merging
gh pr close 123

# Checkout PR locally
gh pr checkout 123
```

## Code Reviews

```bash
# Approve PR
gh pr review 123 --approve

# Request changes
gh pr review 123 --request-changes --body "Please fix X"

# Comment only
gh pr review 123 --comment --body "Looks good overall"

# Add line comment (via API)
gh api repos/{owner}/{repo}/pulls/123/comments \
  -f body="Comment" -f path="file.js" -f line=42 -f side="RIGHT"
```
