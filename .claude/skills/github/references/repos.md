# Repository Operations

## View Repository Information

```bash
# Current repo info
gh repo view

# Specific repo
gh repo view owner/repo

# List branches
gh api repos/{owner}/{repo}/branches --jq '.[].name'

# View commit history
gh api repos/{owner}/{repo}/commits --jq '.[] | "\(.sha[0:7]) \(.commit.message | split("\n")[0])"'

# Browse files in browser
gh browse --repo owner/repo
```

## Create & Manage Repositories

```bash
# Create new public repo
gh repo create repo-name --public --description "Description"

# Create private repo and clone
gh repo create repo-name --private --clone

# Fork a repo
gh repo fork owner/repo --clone

# Clone existing repo
gh repo clone owner/repo
```

## Search

```bash
# Search repositories
gh search repos "query" --limit 10

# Search code in repo
gh search code "pattern" --repo owner/repo
```

## Releases & Tags

```bash
# List releases
gh release list

# View release
gh release view v1.0.0

# Create release
gh release create v1.0.0 --title "Release 1.0.0" --notes "Release notes"

# Create from tag with auto-generated notes
gh release create v1.0.0 --generate-notes

# Upload assets
gh release upload v1.0.0 ./dist/*.zip

# Delete release
gh release delete v1.0.0

# Download release assets
gh release download v1.0.0
```
