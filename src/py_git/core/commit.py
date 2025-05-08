import hashlib
import json

from rich.console import Console
from rich.panel import Panel

from src.py_git.core import BASE_DIR

console = Console()


def commit(message: str) -> None:
    """
    Commit the changes to the repository.
    """
    with open(f"{BASE_DIR}/.py-git/HEAD", "r") as head_file:
        head_content = head_file.read().strip()
        parent = head_content

    prev_index_hash = ""
    if parent != "":
        with open(f"{BASE_DIR}/.py-git/commits/{parent}", "r") as parent_file:
            parent_content = parent_file.read()
            commit_json = json.loads(parent_content)
            prev_index_hash = commit_json["index_hash"]

    with open(f"{BASE_DIR}/.py-git/index", "r") as index_file:
        index_content = index_file.read()
        if index_content == "":
            console.print(
                "[bold red]No changes to commit, please add it first[/bold red]"
            )
            return
        index_hash = hashlib.sha1(index_content.encode()).hexdigest()
        files = index_content.split("\n")

    if prev_index_hash == index_hash:
        console.print("[bold red]No changes to commit, please add it first[/bold red]")
        return

    dic_files = {}
    for file in files:
        if file == "":
            continue
        file = file.split("\t")
        if len(file) < 2:
            continue
        dic_files[file[1]] = file[0]

    content = {
        "message": message,
        "parent": parent,
        "index_hash": index_hash,
        "files": dic_files,
    }

    content_str = json.dumps(content, indent=2)

    # Generate commit hash
    commit_hash = hashlib.sha1(content_str.encode()).hexdigest()

    # Save commit
    with open(f"{BASE_DIR}/.py-git/commits/{commit_hash}", "w") as commit_file:
        commit_file.write(content_str)

    # Update HEAD
    with open(f"{BASE_DIR}/.py-git/HEAD", "w") as head_file:
        head_file.write(commit_hash)

    # Update log
    with open(f"{BASE_DIR}/.py-git/log.txt", "a") as log_file:
        log_file.write(f"{commit_hash} - {message}\n")

    console.print(
        Panel.fit(
            f"[bold green]Commit successful![/bold green]\n"
            f"[yellow]Hash:[/yellow] {commit_hash}\n"
            f"[yellow]Message:[/yellow] {message}",
            title="py-git commit",
            border_style="green",
        )
    )
