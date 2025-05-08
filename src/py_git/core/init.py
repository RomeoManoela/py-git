import os


def init() -> bool:
    """
    Initialize a new py-git repository.
    Creates the .py-git/ directory and necessary subdirectories/files.
    """
    if os.path.exists(".py-git"):
        print("py-git repository already exists")
        return False

    os.makedirs(".py-git", exist_ok=True)

    os.makedirs(".py-git/commits", exist_ok=True)
    os.makedirs(".py-git/objects", exist_ok=True)

    with open(".py-git/index", "w") as index_file:
        index_file.write("")

    with open(".py-git/HEAD", "w") as head_file:
        head_file.write("")

    with open(".py-git/log.txt", "w") as log_file:
        log_file.write("# Commit history\n")

    print("py-git repository initialized successfully.")
    return True
