import os


def current_files() -> list[str]:
    filenames = []
    for root, _, files in os.walk("./"):
        for file in files:
            # Skip .py-git directory and its contents
            if ".py-git" in root:
                continue

            rel_path = os.path.join(root, file)

            if (
                ".py-git" not in rel_path
                and not rel_path.startswith("./.")
                and not file.startswith(".")
            ):
                filenames.append(rel_path[2:])
    return filenames
