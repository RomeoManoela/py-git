import os


def init():
    """
    Initialize a new py-git repository.
    Creates the .py-git/ directory and necessary subdirectories/files.
    """
    # Create the main directory
    os.makedirs(".py-git", exist_ok=True)

    # Create subdirectories
    os.makedirs(".py-git/commits", exist_ok=True)
    os.makedirs(".py-git/objects", exist_ok=True)

    # Create necessary files
    with open(".py-git/index", "w") as index_file:
        index_file.write("")  # Initially empty index file

    with open(".py-git/HEAD", "w") as head_file:
        head_file.write("")  # Initially empty HEAD file

    with open(".py-git/log.txt", "w") as log_file:
        log_file.write("# Commit history\n")

    print("py-git repository initialized successfully.")
