import os
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from src.py_git.core import BASE_DIR
from src.py_git.helpers.commit_files import commit_files
from src.py_git.helpers.current_files import current_files

console = Console()


def checkout(hash_commit: str) -> None:
    """
    Checkout a commit.

    Args:
        hash_commit: The commit hash to check out
    """

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

    curr_files = set(current_files())
    committed_file_paths = set(committed_files.keys())

    # Files to remove (in working directory but not in commit)
    files_to_remove = curr_files - committed_file_paths

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]Checking out files...[/bold blue]"),
        console=console,
    ) as progress:

        restore_task = progress.add_task("Restoring files", total=len(committed_files))

        for file, hash_file in committed_files.items():
            try:
                file_path = Path(f"{BASE_DIR}/{file}")
                file_dir = file_path.parent
                if not file_dir.exists():
                    file_dir.mkdir(parents=True, exist_ok=True)

                with open(
                    f"{BASE_DIR}/.py-git/objects/{hash_file}", "rb"
                ) as file_object:
                    with open(file_path, "wb") as file_current:
                        file_current.write(file_object.read())

                progress.update(restore_task, advance=1)
            except Exception as e:
                console.print(
                    f"[bold red]Error restoring file {file}:[/bold red] {str(e)}"
                )

        if files_to_remove:
            remove_task = progress.add_task(
                "Removing extra files", total=len(files_to_remove)
            )

            for file in files_to_remove:
                try:
                    file_path = Path(f"{BASE_DIR}/{file}")
                    if file_path.exists():
                        file_path.unlink()
                    progress.update(remove_task, advance=1)
                except Exception as e:
                    console.print(
                        f"[bold red]Error removing file {file}:[/bold red] {str(e)}"
                    )

    cleanup_empty_directories(BASE_DIR)

    with open(f"{BASE_DIR}/.py-git/HEAD", "w") as head_file:
        head_file.write(hash_commit)

    console.print(
        Panel(
            f"[bold green]Successfully checked out commit:[/bold green]\n"
            f"[yellow]Commit hash:[/yellow] {hash_commit[:8]}...\n"
            f"[yellow]Files restored:[/yellow] {len(committed_files)}\n"
            f"[yellow]Files removed:[/yellow] {len(files_to_remove)}",
            title="Checkout Complete",
            border_style="green",
        )
    )


def cleanup_empty_directories(base_dir: str) -> None:
    """
    Remove empty directories recursively.

    Args:
        base_dir: Base directory to start from
    """
    for root, dirs, files in os.walk(base_dir, topdown=False):
        # Skip .py-git directory
        if ".py-git" in root:
            continue

        if not files and not dirs:
            try:

                if root != base_dir:
                    os.rmdir(root)
            except OSError:
                pass
