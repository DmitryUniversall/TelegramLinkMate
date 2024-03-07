import os
from typing import Tuple


def get_file(path: str) -> Tuple[str, bytes]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"File '{path}' was not found")

    filename = os.path.split(path)[-1]

    with open(path, "rb") as file:
        file_data = file.read()

    return filename, file_data
