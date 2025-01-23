# Auto_Commit

A Python-based tool for automatically committing changes to a Git repository when a certain number of lines have been modified.

## Features

- Automatic WIP (Work In Progress) commits when changes exceed a threshold
- Configurable repository path via environment file
- Real-time monitoring of Git repository changes
- Customizable commit intervals and thresholds

## Components

The project consists of two Python scripts that work together:

### 1. auto_commit.py
- Monitors a Git repository for changes
- Makes automatic WIP commits when changes exceed 30 lines
- Reads repository path from `.env` file
- Checks every 10 minutes for changes
- Validates Git repository status

### 2. set_env_path.py
- Sets the target repository path
- Saves the path to a `.env` file
- Provides interactive path selection

## Usage

1. First, set your repository path:
```bash
python3 set_env_path.py
```

2. In a separate terminal, start the auto-commit monitor:
```bash
python3 auto_commit.py
```

## Configuration

The following constants can be modified in `auto_commit.py`:
- `CHECK_INTERVAL`: Time between checks (default: 10 minutes)
- `MIN_CHANGED_LINES`: Minimum lines changed to trigger commit (default: 30)
- `COMMIT_MESSAGE`: Template for commit messages

## Requirements

- Python 3.x
- Git installed and configured
- Write access to the target repository

## Notes

- Both scripts should be run in separate terminal windows
- The auto-commit script will continue running until manually stopped
- Changes are tracked through a `.env` file for persistence
