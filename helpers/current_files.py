import os
from pathlib import Path
from typing import List, Set, Optional

from core import BASE_DIR


def current_files(
    ignore_dirs: Optional[Set[str]] = None,
    ignore_patterns: Optional[Set[str]] = None,
    ignore_hidden: bool = True,
) -> List[str]:
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

    if ignore_patterns is None:
        ignore_patterns = {"*.pyc", "*.pyo", "*.pyd", "*.so", "*.dll"}

    base_path = Path(BASE_DIR).resolve()
    print(base_path)
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

            # Add to the list if not already ignored
            if rel_path:
                filenames.append(rel_path)

    return sorted(filenames)
