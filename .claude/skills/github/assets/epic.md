# Epic Template

## Naming Convention

```
Title: Epic <N>: <Title>
Key:   epic-<N>
Label: epic, epic-<N>
```

**Examples:**
- `Epic 1: Streamlined GitOps Command Experience`
- `Epic 2: Payment Processing System`

## Create via Script (Recommended)

```bash
~/.claude/skills/github/scripts/create-epic.sh "Streamlined GitOps Command Experience"
```

The script will:
- Auto-increment the epic number
- Create labels (`epic`, `epic-1`)
- Generate consistent body format
- Add to project board

## Manual Creation

```bash
gh issue create --repo <owner>/<repo> \
  --title "Epic 1: Streamlined GitOps Command Experience" \
  --label "epic,epic-1" \
  --body "$(cat <<'EOF'
**Epic Key:** epic-1
**Status:** Backlog

---

## Goal
Streamline the GitOps command experience for developers.

## Scope
- [ ] Define scope item 1
- [ ] Define scope item 2
- [ ] Define scope item 3

## Out of Scope
- TBD

## Stories
| Key | Title | Status |
|-----|-------|--------|
| epic-1-story-1 | TBD | Backlog |

## Success Metrics
- TBD

---
*This epic tracks the overall progress of Streamlined GitOps Command Experience.*
EOF
)"
```

## Body Format

```markdown
**Epic Key:** epic-<N>
**Status:** Backlog

---

## Goal
<High-level objective>

## Scope
- [ ] Scope item 1
- [ ] Scope item 2

## Out of Scope
- Item 1

## Stories
| Key | Title | Status |
|-----|-------|--------|
| epic-<N>-story-1 | Story title | Backlog |
| epic-<N>-story-2 | Story title | Backlog |

## Success Metrics
- Metric 1
- Metric 2

---
*This epic tracks the overall progress of <Title>.*
```
