# User Story Template

## Naming Convention

```
Title: Story <E>.<S>: <Title>
Key:   epic-<E>-story-<S>
Label: story, epic-<E>
```

**Examples:**
- `Story 1.1: User authentication` (first story in epic 1)
- `Story 2.3: Checkout flow UI` (third story in epic 2)

## Create via Script (Recommended)

```bash
# Create story in epic 1
~/.claude/skills/github/scripts/create-story.sh 1 "User authentication"

# Interactive mode (prompts for epic and title)
~/.claude/skills/github/scripts/create-story.sh
```

The script will:
- Auto-increment the story number within the epic
- Link to parent epic via labels
- Prompt for acceptance criteria
- Generate consistent body format
- Add to project board
- Suggest branch name

## Manual Creation

```bash
gh issue create --repo <owner>/<repo> \
  --title "Story 1.1: User authentication" \
  --label "story,epic-1" \
  --body "$(cat <<'EOF'
**Story Key:** epic-1-story-1
**Epic:** Epic 1: Streamlined GitOps Command Experience
**Status:** Backlog

---

## Description
As a developer, I want to authenticate via GitHub so that I can access protected resources.

## Acceptance Criteria
- [ ] AC1: User can click "Login with GitHub"
- [ ] AC2: OAuth flow completes successfully
- [ ] AC3: User session is created after login
- [ ] AC4: Error messages display for failed auth

## Technical Notes
- Use OAuth 2.0 flow
- Store tokens securely

## Out of Scope
- Multi-factor authentication (future story)

---
*Part of epic-1*
EOF
)"
```

## Body Format

```markdown
**Story Key:** epic-<E>-story-<S>
**Epic:** Epic <E>: <Epic Title>
**Status:** Backlog

---

## Description
As a <user type>, I want to <action> so that <benefit>.

## Acceptance Criteria
- [ ] AC1: <Criterion>
- [ ] AC2: <Criterion>
- [ ] AC3: <Criterion>

## Technical Notes
- Note 1
- Note 2

## Out of Scope
- Item 1

---
*Part of epic-<E>*
```

## Branch Naming

When working on a story, use the GitHub issue number:

```bash
# Story 1.1 created as issue #42
git checkout -b 42-user-authentication
```

This enables board sync: branch with issue number → moves to "In Progress"
