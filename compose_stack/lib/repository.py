import zipfile

import httpx
import rich
import requests


def download_repository_code(repository: str, stack: str, todos: bool):
    zip_file = f"{stack}.zip"
    zip_name = "todos.zip" if todos else "main.zip"
    repository_url = f"https://github.com/{repository}/archive/{zip_name}"
    print(repository_url)
    with open(zip_file, "wb") as download_file:
        with httpx.stream("GET", repository_url, follow_redirects=True) as response:
            for chunk in response.iter_bytes():
                download_file.write(chunk)
