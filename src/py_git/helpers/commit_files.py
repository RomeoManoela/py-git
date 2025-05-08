import json
import os

from rich.console import Console

from src.py_git.core import BASE_DIR

console = Console()


def commit_files(commit_hash: str) -> dict[str, str] | None:
    # Validate commit hash
    commits_dir = f"{BASE_DIR}/.py-git/commits"
    if not os.path.exists(f"{commits_dir}/{commit_hash}"):
        return None
    with open(f"{BASE_DIR}/.py-git/commits/{commit_hash}") as commit_file:
        commit_content = commit_file.read()
        commit_json = json.loads(commit_content)
        return commit_json["files"]
