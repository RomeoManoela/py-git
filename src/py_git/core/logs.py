import os
import sys

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.py_git.core import BASE_DIR

console = Console()


def logs():
    log_path = f"{BASE_DIR}/.py-git/log.txt"
    if not os.path.exists(log_path):
        console.print("[bold red]No commit history found.[/bold red]")
        sys.exit(1)

    with open(log_path, "r") as log_file:
        lines = log_file.readlines()

    # Skip the header line
    commit_lines = [line.strip() for line in lines if not line.startswith("#")]

    if not commit_lines:
        console.print("[bold yellow]No commits yet.[/bold yellow]")
        sys.exit(0)

    table = Table(show_header=True, header_style="bold cyan", box=box.ROUNDED)
    table.add_column("Commit Hash", style="dim")
    table.add_column("Message", style="green")

    for line in commit_lines:
        if " - " in line:
            commit_hash, message = line.split(" - ", 1)
            table.add_row(commit_hash, message)

    console.print(
        Panel(
            table,
            title="[bold blue]Commit History[/bold blue]",
            subtitle=f"[dim]{len(commit_lines)} commits[/dim]",
            border_style="blue",
        )
    )
