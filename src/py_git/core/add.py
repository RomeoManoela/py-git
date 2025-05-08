import hashlib
import os
import shutil
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

from src.py_git.core import BASE_DIR
from src.py_git.helpers.current_files import current_files

console = Console()


def hash_and_store_file(filename: str) -> tuple[str, str, bool]:
    """
    Hash a file and store it in the objects directory if needed.

    Args:
        filename: Path to the file

    Returns:
        Tuple of (filename, hash_value, is_new)
    """
    try:
        with open(filename, "rb") as file:
            data = file.read()

        hash_value = hashlib.sha1(data).hexdigest()
        object_path = Path(f"{BASE_DIR}/.py-git/objects/{hash_value}")

        is_new = False
        if not object_path.exists():
            os.makedirs(object_path.parent, exist_ok=True)
            shutil.copy2(filename, object_path)
            is_new = True

        return filename, hash_value, is_new
    except Exception as e:
        console.print(f"[bold red]Error processing {filename}:[/bold red] {str(e)}")
        return filename, "", False


def add(filenames: list[str]) -> None:
    """
    Add files to the index (staging area).

    Args:
        filenames: List of files to add
    """

    if filenames == ["."]:
        filenames = current_files()
        console.print(
            f"[bold blue]Adding all {len(filenames)} files in working directory[/bold blue]"
        )

    valid_files = [f for f in filenames if os.path.isfile(f)]
    if len(valid_files) < len(filenames):
        skipped = set(filenames) - set(valid_files)
        if skipped:
            console.print(
                f"[bold yellow]Skipping {len(skipped)} non-existent or directory paths[/bold yellow]"
            )

    if not valid_files:
        console.print("[bold red]No valid files to add[/bold red]")
        return

    index_path = f"{BASE_DIR}/.py-git/index"
    existing_entries: dict[str, str] = {}

    if os.path.exists(index_path):
        with open(index_path, "r") as index_file:
            for line in index_file:
                if line.strip():
                    parts = line.strip().split("\t")
                    if len(parts) >= 2:
                        existing_entries[parts[1]] = parts[0]

    # Process files in parallel
    new_count = 0
    updated_count = 0
    updated_entries = existing_entries.copy()

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]Adding files...[/bold blue]"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
    ) as progress:
        task = progress.add_task("Adding", total=len(valid_files))

        with ThreadPoolExecutor(max_workers=min(10, len(valid_files))) as executor:
            futures = [
                executor.submit(hash_and_store_file, filename)
                for filename in valid_files
            ]

            for future in futures:
                filename, hash_value, is_new = future.result()
                if hash_value:
                    if filename not in existing_entries:
                        new_count += 1
                    elif existing_entries[filename] != hash_value:
                        updated_count += 1

                    updated_entries[filename] = hash_value

                progress.update(task, advance=1)

    with open(index_path, "w") as index_file:
        for filename, hash_value in sorted(updated_entries.items()):
            index_file.write(f"{hash_value}\t{filename}\n")

    if new_count > 0 or updated_count > 0:
        console.print(
            f"[bold green]Added {new_count} new and {updated_count} modified files to the index "
            f"({len(updated_entries)} total files tracked)[/bold green]"
        )
    else:
        console.print("[bold yellow]No changes to add[/bold yellow]")
