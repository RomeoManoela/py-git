import os
from pathlib import Path
from typing import Optional

from src.py_git.core import BASE_DIR


def current_files(
    ignore_dirs: Optional[set[str]] = None,
    ignore_patterns: Optional[set[str]] = None,
    ignore_hidden: bool = True,
) -> list[str]:
    """
    Get a list of all files in the current directory, excluding ignored files and directories.

    Args:
        ignore_dirs: Set of directory names to ignore (default: ['.py-git', '.git'])
        ignore_patterns: Set of file patterns to ignore (default: [])
        ignore_hidden: Whether to ignore hidden files and directories (default: True)

    Returns:
        List of relative file paths
    """

    if ignore_dirs is None:
        ignore_dirs = {
            ".py-git",
            ".git",
            "__pycache__",
            "venv",
            ".venv",
            "node_modules",
        }
    gitignore_path = f"{BASE_DIR}/.py-gitignore"
    if os.path.exists(gitignore_path):
        with open(f"{BASE_DIR}/.py-gitignore") as ignore_files:
            for line in ignore_files:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if line.startswith("/"):
                    line = line[:-1]
                ignore_dirs.add(line)
    print(ignore_dirs)

    if ignore_patterns is None:
        ignore_patterns = {"*.pyc", "*.pyo", "*.pyd", "*.so", "*.dll"}

    base_path = Path(BASE_DIR).resolve()
    base_str_len = len(str(base_path)) + 1

    filenames = []

    for root, dirs, files in os.walk(base_path):

        root_path = Path(root)

        # Skip ignored directories
        dirs[:] = [
            d
            for d in dirs
            if (d not in ignore_dirs and not (ignore_hidden and d.startswith(".")))
        ]

        for file in files:
            if ignore_hidden and file.startswith("."):
                continue

            if any(Path(file).match(pattern) for pattern in ignore_patterns):
                continue

            full_path = root_path / file
            rel_path = str(full_path)[base_str_len:]

            if rel_path:
                filenames.append(rel_path)

    return sorted(filenames)
