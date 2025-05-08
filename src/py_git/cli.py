import sys

from src.py_git.core.add import add
from src.py_git.core.checkout import checkout
from src.py_git.core.commit import commit
from src.py_git.core.diff import diff
from src.py_git.core.init import init
from src.py_git.core.logs import logs
from src.py_git.core.status import status
from src.py_git.helpers.is_a_repos import is_a_repo


def show_help():
    print("py-git: A mini version control system written in Python")
    print("\nAvailable commands:")
    print("  init                  Initialize a new py-git repository")
    print("  add <files>           Add files to the staging area")
    print("  commit <message>      Record changes to the repository")
    print("  status                Show the working tree status")
    print("  logs                  Display commit history")
    print("  diff <file>           Show changes between working tree and last commit")
    print("  checkout <hash>       Switch to a specific commit")
    print("\nOptions:")
    print("  -h, --help            Display this help message")


def main():
    if len(sys.argv) < 2:
        print("Usage: py-git <command> [args]")
        print("Try 'py-git --help' for more information")
        sys.exit(1)

    command = sys.argv[1]

    if command in ["-h", "--help"]:
        show_help()
        return

    if command == "init":
        init()
        return

    is_a_repo()

    if command == "add":
        if len(sys.argv) < 3:
            print("Usage: py-git add <filenames>")
            sys.exit(1)
        if sys.argv[2] == ".":
            filenames = ["."]
        else:
            filenames = sys.argv[2:]
        add(filenames)

    elif command == "commit":
        if len(sys.argv) < 3:
            print("Usage: py-git commit <message>")
            sys.exit(1)
        message = sys.argv[2]
        commit(message)

    elif command == "diff":
        if len(sys.argv) < 3:
            print("Usage: py-git diff <filename>")
            sys.exit(1)
        filename = sys.argv[2]
        diff(filename)

    elif command == "logs":
        logs()

    elif command == "status":
        status()

    elif command == "checkout":
        if len(sys.argv) < 3:
            print("Usage: py-git checkout <commit_hash>")
            sys.exit(1)
        hash_commit = sys.argv[2]
        checkout(hash_commit)

    else:
        print(f"Unknown command: {command}, loot at --help or -h")
        sys.exit(1)


if __name__ == "__main__":
    main()
