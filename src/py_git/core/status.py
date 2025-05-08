import hashlib

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.py_git.core import BASE_DIR
from src.py_git.helpers.commit_files import commit_files
from src.py_git.helpers.current_files import current_files

console = Console()


def status():
    """
    Show the working tree status, similar to git status.
    """

    with open(f"{BASE_DIR}/.py-git/HEAD", "r") as head_file:
        head_content = head_file.read().strip()
        if head_content == "":
            console.print("[bold yellow]No commits yet[/bold yellow]")
            current_head = None
        else:
            current_head = head_content

    committed_files = {}
    if current_head:
        committed_files = commit_files(current_head)

    # Get files from the index (staged)
    staged_files = {}
    with open(f"{BASE_DIR}/.py-git/index", "r") as index_file:
        for line in index_file:
            if line.strip():
                parts = line.strip().split("\t")
                if len(parts) >= 2:
                    staged_files[parts[1]] = parts[0]

    working_files = {}
    curr_files: list[str] = current_files()
    for curr_file in curr_files:
        with open(f"{BASE_DIR}/{curr_file}", "rb") as f:
            content = f.read()
            working_files[curr_file] = hashlib.sha1(content).hexdigest()

    staged_new = []
    staged_modified = []
    modified = []
    untracked = []

    # Check staged files against committed files
    for file, hash_value in staged_files.items():
        if file not in committed_files:
            staged_new.append(file)
        elif committed_files[file] != hash_value:
            staged_modified.append(file)

    # Check working files against staged files
    for file, hash_value in working_files.items():
        if file not in staged_files and file not in committed_files:
            untracked.append(file)
        elif file in staged_files and staged_files[file] != hash_value:
            modified.append(file)

    if current_head:
        console.print(f"[bold blue]On commit:[/bold blue] {current_head}")

    # Tables for different categories
    if staged_new or staged_modified:
        staged_table = Table(show_header=True, header_style="green", box=box.SIMPLE)
        staged_table.add_column("Status")
        staged_table.add_column("File")

        for file in staged_new:
            staged_table.add_row("new file", file)
        for file in staged_modified:
            staged_table.add_row("modified", file)

        console.print(
            Panel(
                staged_table,
                title="[bold green]Changes to be committed[/bold green]",
                border_style="green",
            )
        )

    if modified:
        modified_table = Table(show_header=True, header_style="red", box=box.SIMPLE)
        modified_table.add_column("Status")
        modified_table.add_column("File")

        for file in modified:
            modified_table.add_row("modified", file)

        console.print(
            Panel(
                modified_table,
                title="[bold red]Changes not staged for commit[/bold red]",
                border_style="red",
            )
        )

    if untracked:
        untracked_table = Table(show_header=False, box=box.SIMPLE)
        untracked_table.add_column("File", style="yellow")

        for file in untracked:
            untracked_table.add_row(file)

        console.print(
            Panel(
                untracked_table,
                title="[bold yellow]Untracked files[/bold yellow]",
                border_style="yellow",
            )
        )

    if not staged_new and not staged_modified and not modified and not untracked:
        console.print("[bold green]Working tree clean[/bold green]")
