import os

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from core import BASE_DIR
from core.commit_files import commit_files

console = Console()


def checkout(hash_commit: str) -> None:
    """
    Checkout a commit.
    """

    commits_dir = f"{BASE_DIR}/.py-git/commits"
    if not os.path.exists(f"{commits_dir}/{hash_commit}"):
        console.print(
            Panel(
                f"[bold red]Error:[/bold red] Commit [bold yellow]{hash_commit}[/bold yellow] not found",
                title="Checkout Failed",
                border_style="red",
            )
        )
        return

    committed_files: dict[str, str] = commit_files(hash_commit)
    if not committed_files:
        console.print(
            Panel(
                "[bold yellow]Warning:[/bold yellow] No files in this commit",
                title="Empty Commit",
                border_style="yellow",
            )
        )
        return

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]Checking out files...[/bold blue]"),
        console=console,
    ) as progress:
        task = progress.add_task("Checking out", total=len(committed_files))

        for file, hash_file in committed_files.items():
            try:

                file_dir = os.path.dirname(f"{BASE_DIR}/{file}")
                if file_dir and not os.path.exists(file_dir):
                    os.makedirs(file_dir, exist_ok=True)

                with open(
                    f"{BASE_DIR}/.py-git/objects/{hash_file}", "rb"
                ) as file_object:
                    with open(f"{BASE_DIR}/{file}", "wb") as file_current:
                        file_current.write(file_object.read())

                progress.update(task, advance=1)
            except Exception as e:
                console.print(
                    f"[bold red]Error restoring file {file}:[/bold red] {str(e)}"
                )

    # Update HEAD
    with open(f"{BASE_DIR}/.py-git/HEAD", "w") as head_file:
        head_file.write(hash_commit)

    console.print(
        Panel(
            f"[bold green]Successfully checked out commit:[/bold green]\n"
            f"[yellow]Commit hash:[/yellow] {hash_commit}...\n"
            f"[yellow]Files restored:[/yellow] {len(committed_files)}",
            title="Checkout Complete",
            border_style="green",
        )
    )
