---
name: github
description: Manage GitHub repositories, issues, pull requests, projects/storyboards, workflows, and security using the gh CLI. Use for any GitHub operations including kanban board management.
license: MIT
compatibility: Requires gh CLI installed and authenticated. Works with Claude Code and similar AI coding assistants.
metadata:
  author: HVN-Labs
  version: "1.0"
---

# GitHub Operations

Manage GitHub via the `gh` CLI. For detailed commands, see reference files.

## Config Loading

**On activation, read `github-config.yaml` from project root.**

```bash
cat github-config.yaml
```

If not found, tell user:
> "No github config found. Create `github-config.yaml` in project root with your board IDs. See `assets/github-config.yaml` for the template."

**Use config values as variables:**
- `$REPO` → `repo`
- `$OWNER` → `owner`
- `$DEFAULT_BASE` → `default_base`
- `$PROJECT_NUMBER` → `project_number`
- `$PROJECT_ID` → `project_id`
- `$STATUS_FIELD_ID` → `status_field_id`
- Status option IDs from `statuses` object

**Example usage with config:**
```bash
# Instead of hardcoding:
gh project item-add 12 --owner your-org --url $URL

# Use config values:
gh project item-add $PROJECT_NUMBER --owner $OWNER --url $URL
```

---

## Prerequisites

```bash
gh --version      # Verify installed
gh auth status    # Verify authenticated
gh auth login     # Authenticate if needed
```

## Behavior Rules

1. **Load config first** - Read `github-config.yaml` before any project operations
2. **Confirm destructive operations** - Ask before delete, merge, close
3. **Return URLs** - Use `--json url --jq '.url'` after creating resources
4. **Handle errors** - Explain failures and suggest fixes
5. **Use JSON for parsing** - Add `--json` flag to extract data

---

## Quick Reference

### Repositories
```bash
gh repo view                              # Current repo info
gh repo view $REPO                        # This project's repo
gh repo create name --public              # Create repo
gh repo clone owner/repo                  # Clone repo
```
→ Full details: `references/repos.md`

### Issues
```bash
gh issue list                             # List open issues
gh issue list --label "bug"               # Filter by label
gh issue view 123                         # View issue
gh issue create --title "T" --body "B"    # Create issue
gh issue close 123                        # Close issue
```
→ Full details: `references/issues.md`

### Pull Requests
```bash
gh pr list                                # List open PRs
gh pr view 123                            # View PR
gh pr create --title "T" --base $DEFAULT_BASE  # Create PR (uses config)
gh pr merge 123 --squash                  # Merge PR
gh pr review 123 --approve                # Approve PR
```
→ Full details: `references/pull-requests.md`

### Projects (Storyboards)
```bash
# Using config values:
gh project list --owner $OWNER
gh project item-list $PROJECT_NUMBER --owner $OWNER
gh project item-add $PROJECT_NUMBER --owner $OWNER --url $ISSUE_URL
gh project item-create $PROJECT_NUMBER --owner $OWNER --title "T" --body "B"

# Move item to "In Progress" (using config status IDs):
gh project item-edit --project-id $PROJECT_ID --id $ITEM_ID \
  --field-id $STATUS_FIELD_ID --single-select-option-id $IN_PROGRESS_OPTION_ID
```
→ Full details: `references/projects.md`
→ Story templates: `assets/`

### Workflows
```bash
gh workflow list                          # List workflows
gh run list                               # List runs
gh run list --status failure              # Failed runs
gh workflow run name.yml                  # Trigger workflow
gh run view RUN_ID --log                  # View logs
```
→ Full details: `references/workflows.md`

### Security
```bash
gh api repos/$REPO/code-scanning/alerts              # Code scanning
gh api repos/$REPO/dependabot/alerts                 # Dependabot
gh api repos/$REPO/secret-scanning/alerts            # Secrets
```
→ Full details: `references/security.md`

---

## Common Patterns

**Get current repo:**
```bash
gh repo view --json owner,name --jq '"\(.owner.login)/\(.name)"'
```

**Create issue and add to board:**
```bash
# Create issue
ISSUE_URL=$(gh issue create --title "Title" --body "Body" --json url --jq '.url')

# Add to project board (using config)
gh project item-add $PROJECT_NUMBER --owner $OWNER --url "$ISSUE_URL"
```

**Move item to status (using config):**
```bash
gh project item-edit --project-id $PROJECT_ID --id $ITEM_ID \
  --field-id $STATUS_FIELD_ID --single-select-option-id $DONE_OPTION_ID
```

**Find PR for current branch:**
```bash
gh pr view --json number,title,url
```

---

## Reference Files

| File | Contents |
|------|----------|
| `references/repos.md` | Repository view, create, fork, clone, search |
| `references/issues.md` | Issue CRUD, labels, comments, search |
| `references/pull-requests.md` | PR create, review, merge, diff |
| `references/projects.md` | Project boards, items, fields, workflows |
| `references/workflows.md` | CI/CD, runs, logs, artifacts, releases |
| `references/security.md` | Code scanning, Dependabot, secrets, notifications |

## Templates

| File | Use For |
|------|---------|
| `assets/github-config.yaml` | Project config template (copy to each project) |
| `assets/user-story.md` | Standard user stories with acceptance criteria |
| `assets/epic.md` | Epics with scope and story breakdown |
| `assets/bug-report.md` | Bug reports with reproduction steps |
| `assets/tech-task.md` | Technical tasks with rollback plans |

---

## Best Practices

1. **Load config first** - Always check for `github-config.yaml` before project board operations
2. **Confirm destructive operations** - Before deleting, merging, or closing, summarize and ask for confirmation
3. **Provide URLs** - After creating resources, provide the GitHub URL using `--json url --jq '.url'`
4. **Use config variables** - Use `$PROJECT_NUMBER`, `$OWNER`, etc. instead of hardcoded values
5. **Handle missing config** - If config not found, guide user to create it
