import hashlib
import json

from core import BASE_DIR


def commit(message: str) -> None:
    """
    Commit the changes to the repository.
    """
    with open(f"{BASE_DIR}/.py-git/HEAD", "r") as head_file:
        head_content = head_file.read().strip()
        if head_content == "":
            parent = ""
        else:
            parent = head_content

    with open(f"{BASE_DIR}/.py-git/index", "r") as index_file:
        index_content = index_file.read()
        files = index_content.split("\n")

    dic_files = {}
    for file in files:
        if file == "":
            continue
        file = file.split("\t")
        if len(file) < 2:
            continue
        dic_files[file[1]] = file[0]

    content = {
        "message": message,
        "files": dic_files,
        "parent": parent,
    }

    # Convert content to JSON string
    content_str = json.dumps(content, indent=2)

    # Generate commit hash
    commit_hash = hashlib.sha1(content_str.encode()).hexdigest()

    # Save commit
    with open(f"{BASE_DIR}/.py-git/commits/{commit_hash}", "w") as commit_file:
        commit_file.write(content_str)

    # Update HEAD
    with open(f"{BASE_DIR}/.py-git/HEAD", "w") as head_file:
        head_file.write(commit_hash)

    # Update log
    with open(f"{BASE_DIR}/.py-git/log.txt", "a") as log_file:
        log_file.write(f"{commit_hash} - {message}\n")

    print(f"Committed: {commit_hash}")


commit("Initial commit")
