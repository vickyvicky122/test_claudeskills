# Bug Report Template

## As Draft Item (board only)

```bash
gh project item-create <PROJECT_NUMBER> --owner <OWNER> \
  --title "Bug: <Short description>" \
  --body "$(cat <<'EOF'
## Bug Description
<What is happening incorrectly>

## Steps to Reproduce
1. <Step 1>
2. <Step 2>
3. <Step 3>
4. Observe: <what happens>

## Expected Behavior
<What should happen>

## Actual Behavior
<What is happening instead>

## Environment
- Browser: <browser and version>
- OS: <operating system>
- Device: <device type>

## Severity
<Critical/High/Medium/Low>

## Workaround
<Temporary workaround if any>
EOF
)"
```

## As Full Issue (trackable)

```bash
gh issue create --repo <owner>/<repo> \
  --title "Bug: <Short description>" \
  --label "bug,<severity>,<area>" \
  --body "$(cat <<'EOF'
## Bug Description
<What is happening incorrectly>

## Steps to Reproduce
1. <Step 1>
2. <Step 2>
3. <Step 3>
4. Observe: <what happens>

## Expected Behavior
<What should happen>

## Actual Behavior
<What is happening instead>

## Environment
- Browser: <browser and version>
- OS: <operating system>
- Device: <device type>
- Version: <app version>

## Severity
<Critical/High/Medium/Low>

## Impact
<How many users affected, business impact>

## Workaround
<Temporary workaround if any>

## Screenshots/Logs
<Attach if available>
EOF
)" --json url --jq '.url'
```

## Example

```bash
gh issue create --repo myorg/myapp \
  --title "Bug: Login fails on Safari" \
  --label "bug,critical,auth" \
  --body "$(cat <<'EOF'
## Bug Description
Users on Safari 17+ cannot log in. Form submission hangs indefinitely.

## Steps to Reproduce
1. Open Safari 17 on macOS Sonoma
2. Navigate to /login
3. Enter valid credentials
4. Click "Sign In"
5. Observe: spinner never stops, no error shown

## Expected Behavior
User should be logged in and redirected to dashboard.

## Actual Behavior
Infinite loading state with no feedback.

## Environment
- Browser: Safari 17.2
- OS: macOS 14.2
- Device: MacBook Pro M3

## Severity
Critical - blocks all Safari users

## Workaround
Use Chrome or Firefox
EOF
)" --json url --jq '.url'
```
