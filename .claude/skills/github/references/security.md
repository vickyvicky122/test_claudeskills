# Security Operations

## Code Scanning Alerts

```bash
# List code scanning alerts
gh api repos/{owner}/{repo}/code-scanning/alerts --jq '.[] | "\(.number) \(.rule.severity) \(.state) \(.rule.description)"'

# Get specific alert
gh api repos/{owner}/{repo}/code-scanning/alerts/ALERT_NUMBER
```

## Dependabot Alerts

```bash
# List Dependabot alerts
gh api repos/{owner}/{repo}/dependabot/alerts --jq '.[] | "\(.number) \(.severity) \(.state) \(.dependency.package.name)"'

# Get specific alert
gh api repos/{owner}/{repo}/dependabot/alerts/ALERT_NUMBER

# Dismiss alert
gh api repos/{owner}/{repo}/dependabot/alerts/ALERT_NUMBER -X PATCH -f state="dismissed" -f dismissed_reason="tolerable_risk"
```

## Secret Scanning

```bash
# List secret scanning alerts
gh api repos/{owner}/{repo}/secret-scanning/alerts --jq '.[] | "\(.number) \(.state) \(.secret_type)"'

# Get specific alert
gh api repos/{owner}/{repo}/secret-scanning/alerts/ALERT_NUMBER
```

---

# Discussions

```bash
# List discussions
gh api repos/{owner}/{repo}/discussions --jq '.[] | "\(.number) \(.title)"'

# View discussion (via browser)
gh browse discussions/123
```

---

# Notifications

```bash
# List notifications
gh api notifications --jq '.[] | "\(.subject.type) \(.subject.title)"'

# Mark all as read
gh api notifications -X PUT -f read=true

# List repo notifications
gh api repos/{owner}/{repo}/notifications
```

---

# User & Organization

```bash
# View authenticated user
gh api user --jq '.login'

# View user profile
gh api users/username

# List organizations
gh api user/orgs --jq '.[].login'

# List org members
gh api orgs/{org}/members --jq '.[].login'

# List teams
gh api orgs/{org}/teams --jq '.[].name'
```

---

# Gists

```bash
# List gists
gh gist list

# Create gist
gh gist create file.txt --public --desc "Description"

# Create from multiple files
gh gist create file1.txt file2.txt

# View gist
gh gist view GIST_ID

# Edit gist
gh gist edit GIST_ID

# Delete gist
gh gist delete GIST_ID
```
