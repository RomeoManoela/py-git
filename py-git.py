import sys

from core.add import add
from core.checkout import checkout
from core.commit import commit
from core.diff import diff
from core.init import init
from core.logs import logs
from core.status import status
from helpers.is_a_repos import is_a_repo

command = sys.argv[1]


if command == "init":
    init()

is_a_repo()

if command == "add":
    if len(sys.argv) < 3:
        print("Usage: py-git add <filenames>")
        sys.exit(1)
    filename: list[str] = []
    if len(sys.argv) == 3 and sys.argv[2] == ".":
        filename = ["."]

    filenames = sys.argv[2:]
    add(filenames)

if command == "commit":
    if len(sys.argv) < 3:
        print("Usage: py-git commit <message>")
        sys.exit(1)
    message = sys.argv[2]
    commit(message)


if command == "diff":
    if len(sys.argv) < 3:
        print("Usage: py-git diff <filename>")
        sys.exit(1)
    filename = sys.argv[2]
    diff(filename)


if command == "logs":
    logs()


if command == "status":
    status()


if command == "checkout":
    if len(sys.argv) < 3:
        print("Usage: py-git checkout <commit_hash>")
        sys.exit(1)
    hash_commit = sys.argv[2]
    checkout(hash_commit)
