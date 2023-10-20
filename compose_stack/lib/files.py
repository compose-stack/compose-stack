import os
from typing import List
import shutil
import zipfile


"""
ARCHIVES
"""


def extract_archive(archive_name: str, destination: str):
    with zipfile.ZipFile(archive_name, "r") as zip_ref:
        zip_ref.extractall(destination)


"""
FILES
"""


def copy_file(source_file: str, destination_file: str, override=False):
    if os.path.exists(destination_file):
        if override:
            delete_files([destination_file])
        else:
            return
    shutil.copy(source_file, destination_file)


def delete_files(files: List[str]):
    for file in files:
        if os.path.exists(file):
            os.remove(file)


"""
FOLDERS
"""


def create_folder(dir: str):
    os.makedirs(dir, exist_ok=True)


def copy_folder(source_dir: str, destination_dir: str, ignore=None):
    shutil.copytree(source_dir, destination_dir, ignore=ignore, dirs_exist_ok=True)


def delete_folders(folders: List[str]):
    for folder in folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)


"""
SPECIFIC FUNCTIONS
"""


def merge_gitignore(destination: str, source: str):
    current_content = []
    if os.path.exists(destination):
        with open(destination, "r") as destination_h:
            current_content = destination_h.readlines()

    with open(destination, "a") as destination_h:
        with open(source, "r") as source_h:
            destination_h.writelines(
                [line for line in source_h if line not in current_content]
            )
