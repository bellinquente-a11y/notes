# Git — Basic Usage

## What is Git?
Git is a distributed version control system used to track changes in code and collaborate safely.
Under the hood, commits, branches, and history are all built from a small [object model](internals.md).

## Typical Workflow

```bash
# Create or enter a project
mkdir my_project && cd my_project

# Initialize a git repository
git init

# Check current status
git status

# Add files to staging
git add file.py
git add .

# Save a snapshot (commit)
git commit -m "Initial commit"

# View commit history
git log --oneline

# Connect to remote repository
git remote add origin <repo-url>

# Upload code
git push -u origin main

# Download latest changes
git pull
```