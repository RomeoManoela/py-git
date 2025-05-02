import hashlib
import os
import shutil


def add(filenames: list[str]) -> None:
    """Add files to the index.(staging area)"""
    if filenames == ["."]:  # all files
        filenames = os.listdir()
    for filename in filenames:
        if os.path.isfile(filename):
            with open(filename, "rb") as index_file:
                data: bytes = index_file.read()
            hash_value = hashlib.sha1(data).hexdigest()
            with open(".py-git/index", "a") as index:
                index.write(f"{hash_value}\t{filename}\n")

            shutil.copy2(filename, f".py-git/objects/{hash_value}")
