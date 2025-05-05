import hashlib
import os
import shutil

from rich.console import Console

from core import BASE_DIR
from helpers.current_files import current_files

console = Console()


def add(filenames: list[str]) -> None:
    """Add files to the index (staging area)."""
    # Handle the special case of adding all files
    if filenames == ["."]:
        filenames = current_files()

    index_path = f"{BASE_DIR}/.py-git/index"
    existing_entries = {}

    if os.path.exists(index_path):
        with open(index_path, "r") as index_file:
            for line in index_file:
                if line.strip():
                    parts = line.strip().split("\t")
                    if len(parts) >= 2:
                        existing_entries[parts[1]] = parts[0]

    updated_entries = existing_entries.copy()
    added_count = 0

    for filename in filenames:
        if os.path.isfile(filename):
            with open(filename, "rb") as file:
                data: bytes = file.read()
            hash_value = hashlib.sha1(data).hexdigest()

            updated_entries[filename] = hash_value

            object_path = f"{BASE_DIR}/.py-git/objects/{hash_value}"
            if not os.path.exists(object_path):

                os.makedirs(os.path.dirname(object_path), exist_ok=True)
                shutil.copy2(filename, object_path)

            added_count += 1

    with open(index_path, "w") as index_file:
        for filename, hash_value in updated_entries.items():
            index_file.write(f"{hash_value}\t{filename}\n")

    console.print(f"[bold green]Added {added_count} files to the index.[/bold green]")
