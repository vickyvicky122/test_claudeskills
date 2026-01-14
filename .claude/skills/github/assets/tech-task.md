# Technical Task Template

## As Draft Item (board only)

```bash
gh project item-create <PROJECT_NUMBER> --owner <OWNER> \
  --title "Tech: <Task description>" \
  --body "$(cat <<'EOF'
## Objective
<What needs to be accomplished>

## Tasks
- [ ] <Task 1>
- [ ] <Task 2>
- [ ] <Task 3>
- [ ] <Task 4>

## Rollback Plan
1. <Rollback step 1>
2. <Rollback step 2>
3. <Rollback step 3>

## Dependencies
- <Dependency 1>
- <Dependency 2>

## Risk Assessment
<Low/Medium/High> - <reason>
EOF
)"
```

## As Full Issue (trackable)

```bash
gh issue create --repo <owner>/<repo> \
  --title "Tech: <Task description>" \
  --label "tech,<area>,<priority>" \
  --body "$(cat <<'EOF'
## Objective
<What needs to be accomplished>

## Background
<Why this is needed>

## Tasks
- [ ] <Task 1>
- [ ] <Task 2>
- [ ] <Task 3>
- [ ] <Task 4>

## Rollback Plan
1. <Rollback step 1>
2. <Rollback step 2>
3. <Rollback step 3>

## Dependencies
- <Dependency 1>
- <Dependency 2>

## Risk Assessment
<Low/Medium/High> - <reason>

## Testing Plan
- <How to verify success>

## Monitoring
- <What to watch after deployment>
EOF
)" --json url --jq '.url'
```

## Example

```bash
gh project item-create 1 --owner @me \
  --title "Tech: Migrate database to PostgreSQL 16" \
  --body "$(cat <<'EOF'
## Objective
Upgrade production database from PostgreSQL 14 to 16 for performance improvements.

## Tasks
- [ ] Test migration on staging environment
- [ ] Backup production database
- [ ] Schedule maintenance window
- [ ] Execute migration
- [ ] Verify data integrity
- [ ] Update connection strings
- [ ] Monitor performance metrics

## Rollback Plan
1. Stop application servers
2. Restore from pre-migration backup
3. Revert connection strings
4. Restart application servers

## Dependencies
- DBA approval
- 2-hour maintenance window
- Staging environment available

## Risk Assessment
Medium - well-documented upgrade path, but production data involved
EOF
)"
```
