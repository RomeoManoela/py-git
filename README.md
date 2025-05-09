github: https://github.com/RomeoManoela/py-git
# minipygit (py-git)

A mini version control system written in Python, inspired by Git.

## Overview

minipygit is a lightweight version control system that implements the core functionality of Git.
It's designed to be simple and functional for basic version control needs.

## Features

- Initialize a repository
- Stage files for commit
- Commit changes with messages
- View repository status
- View commit history
- Compare file differences
- Checkout previous commits

## Installation

```bash

pip install minipygit
```

## Usage

for ignored files, create a .py-gitignore file in the root of your repository and add the files you want to ignore

```bash
# Initialize a new repository
py-git init

# Add files to staging area
py-git add file.txt
py-git add .  # Add all files

# Commit changes
py-git commit "Add initial files"

# Check repository status
py-git status

# View commit history
py-git logs

# View differences in a file
py-git diff file.txt

# Checkout a specific commit
py-git checkout <commit_hash>

# Display help
py-git --help
```

- Python 3.12 or higher
