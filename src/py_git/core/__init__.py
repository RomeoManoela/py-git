import os
from pathlib import Path


def find_repository_root():
    """
    Find the root directory of the py-git repository by looking for common project indicators.

    Starts from the current working directory and traverses up the directory tree
    until it finds a directory that appears to be a project root or reaches the filesystem root.

    Project root indicators:
    - .py-git directory (primary indicator for py-git repositories)
    - Common project files: pyproject.toml, setup.py, requirements.txt
    - Common project directories: .git, .venv, venv

    Returns:
        str: The repository root path, or the current directory if not found
    """
    current_dir = Path(os.getcwd()).resolve()

    # Files and directories that indicate a project root
    root_indicators = [
        ".git",
        ".venv",
        "venv",
        ".idea",
        ".vscode",
        ".py-git",
        "pyproject.toml",
        "main.py",
        "requirements.txt",
    ]

    while current_dir != current_dir.parent:

        for indicator in root_indicators[1:]:
            if (current_dir / indicator).exists():
                return str(current_dir)

        current_dir = current_dir.parent

    # If we didn't find any indicators, return the current directory
    # This will be the case when initializing a new repository
    return os.getcwd()


BASE_DIR = find_repository_root()
