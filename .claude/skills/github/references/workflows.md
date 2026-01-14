# Workflows & CI/CD

## View Workflows

```bash
# List workflows
gh workflow list

# List workflow runs
gh run list

# Filter by workflow
gh run list --workflow "CI"

# Filter by branch
gh run list --branch main

# Filter by status
gh run list --status failure

# View specific run
gh run view RUN_ID

# View run with jobs
gh run view RUN_ID --verbose
```

## Trigger & Manage Runs

```bash
# Trigger workflow
gh workflow run workflow-name.yml

# Trigger with inputs
gh workflow run workflow-name.yml -f input1=value1 -f input2=value2

# Trigger on specific branch
gh workflow run workflow-name.yml --ref feature-branch

# Cancel run
gh run cancel RUN_ID

# Rerun failed jobs
gh run rerun RUN_ID --failed

# Rerun all jobs
gh run rerun RUN_ID
```

## Logs & Artifacts

```bash
# View logs
gh run view RUN_ID --log

# View failed logs only
gh run view RUN_ID --log-failed

# Download artifacts
gh run download RUN_ID

# Download specific artifact
gh run download RUN_ID -n artifact-name

# Watch run in progress
gh run watch RUN_ID
```
