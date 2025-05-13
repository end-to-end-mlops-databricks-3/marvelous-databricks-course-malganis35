#!/bin/bash

# Step 1: Fetch the latest remote branches from origin
git fetch origin

# Step 2: Create local branches from remote ones (origin/*)
for branch in $(git branch -r | grep '^  origin/' | grep -v 'HEAD' | sed 's|origin/||'); do
  git show-ref --verify --quiet "refs/heads/$branch"
  if [ $? -ne 0 ]; then
    echo "Creating local branch: $branch"
    git checkout -b "$branch" "origin/$branch"
  else
    echo "Branch $branch already exists locally"
  fi
done

# Step 3: Switch back to the main branch (or master depending on the project)
git checkout main 2>/dev/null || git checkout master

# Step 4: Push all local branches to GitLab
git push --all gitlab
