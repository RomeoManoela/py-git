import json
from itertools import zip_longest

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from src.py_git.core import BASE_DIR

console = Console()


def diff(filename):
    with open(f"{BASE_DIR}/.py-git/HEAD", "r") as head_file:
        head_content = head_file.read().strip()
        current_head = head_content
        if current_head == "":
            console.print("[bold red]No commits yet[/bold red]")
            return
        with open(f"{BASE_DIR}/.py-git/commits/{current_head}") as commit_file:
            commit_content = commit_file.read()
            commit_json = json.loads(commit_content)

            if filename not in commit_json["files"]:
                console.print(
                    f"[bold yellow]File [/bold yellow][bold cyan]{filename}[/bold cyan][bold yellow] not found in commit[/bold yellow]"
                )
                return

            file_hash = commit_json["files"][filename]

            console.print(
                Panel.fit(
                    f"[bold cyan]Comparing [/bold cyan][bold green]{filename}[/bold green]",
                    subtitle=f"Commit: {current_head[:8]}",
                    border_style="blue",
                )
            )

            with (
                open(f"{BASE_DIR}/.py-git/objects/{file_hash}") as file_object,
                open(f"{BASE_DIR}/{filename}") as file_current,
            ):
                has_differences = False

                for i, (line, curr_line) in enumerate(
                    zip_longest(file_object, file_current)
                ):
                    if line != curr_line:
                        has_differences = True

                        line_num = Text(f"Line {i+1}:", style="bold yellow")

                        old_text = Text(
                            f"{line.rstrip() if line else '(empty)'}", style="red"
                        )
                        new_text = Text(
                            f"{curr_line.rstrip() if curr_line else '(empty)'}",
                            style="green",
                        )

                        console.print(line_num, " ")
                        console.print("- ", old_text)
                        console.print("+ ", new_text)

                if not has_differences:
                    console.print("[bold green]No differences found![/bold green]")
