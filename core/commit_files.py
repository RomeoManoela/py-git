import json
import os

from rich.console import Console
from rich.panel import Panel

from core import BASE_DIR

console = Console()


def commit_files(commit_hash: str) -> dict[str, str] | None:
    # Validate commit hash
    commits_dir = f"{BASE_DIR}/.py-git/commits"
    if not os.path.exists(f"{commits_dir}/{commit_hash}"):
        console.print(
            Panel(
                f"[bold red]Error:[/bold red] Commit [bold yellow]{commit_hash}[/bold yellow] not found",
                title="Checkout Failed",
                border_style="red",
            )
        )
        return None
    with open(f"{BASE_DIR}/.py-git/commits/{commit_hash}") as commit_file:
        commit_content = commit_file.read()
        commit_json = json.loads(commit_content)
        return commit_json["files"]
