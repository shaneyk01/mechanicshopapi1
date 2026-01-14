# GitHub Actions Workflow Guide

This guide explains how to run the GitHub Actions workflows in this repository.

## Available Workflows

### Flask CI Workflow
**File:** `.github/workflows/main.yaml`

This workflow automatically tests the Flask application by:
1. Setting up Python 3.12
2. Creating a virtual environment
3. Installing dependencies from `requirements.txt`
4. Running debugging information

## How to Run the Workflow

There are **three ways** to trigger the workflow:

### 1. Automatic Trigger on Push (Default)
The workflow automatically runs when you push commits to the `main` or `master` branches.

```bash
# Make your changes
git add .
git commit -m "Your commit message"
git push origin main  # or master
```

### 2. Manual Trigger via GitHub Web Interface (Recommended)
You can manually trigger the workflow from GitHub's web interface:

1. Go to your repository on GitHub: https://github.com/shaneyk01/mechanicshopapi1
2. Click on the **"Actions"** tab at the top of the page
3. In the left sidebar, click on **"Flask CI"** workflow
4. Click the **"Run workflow"** button (appears on the right side)
5. Select the branch you want to run the workflow on
6. Click the green **"Run workflow"** button to confirm

### 3. Merge Your Branch to Main/Master
If you're working on a feature branch (like `copilot/run-workflow-pipeline`):

```bash
# First, make sure your branch is pushed
git push origin your-branch-name

# Then create a Pull Request on GitHub to merge into main/master
# Or merge locally:
git checkout main
git merge your-branch-name
git push origin main
```

## Viewing Workflow Results

1. Go to the **Actions** tab on GitHub
2. Click on a specific workflow run to see details
3. Click on individual jobs (like "build") to see logs
4. Green checkmark ✅ = Success
5. Red X ❌ = Failure

## Troubleshooting

### Workflow Doesn't Appear in Actions Tab
- Make sure the workflow file is in `.github/workflows/` directory
- Ensure the file has a `.yaml` or `.yml` extension
- Check that the file is pushed to GitHub

### Workflow Doesn't Run Automatically
- Verify you pushed to the correct branch (`main` or `master`)
- Check the workflow file's `on:` section to see which events trigger it

### Workflow Fails
- Click on the failed workflow run in the Actions tab
- Expand the failed step to see error messages
- Common issues:
  - Missing dependencies in `requirements.txt`
  - Python version mismatch
  - Syntax errors in the workflow YAML file

## Current Workflow Status

To check if your workflow is currently running or view past runs:
1. Visit: https://github.com/shaneyk01/mechanicshopapi1/actions
2. Look for recent workflow runs with their status

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Actions Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
