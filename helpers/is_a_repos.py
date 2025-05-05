import os
import sys


def is_a_repo() -> None:
    if not os.path.exists(".py-git"):
        print("Not a py-git repository")
        sys.exit(1)
