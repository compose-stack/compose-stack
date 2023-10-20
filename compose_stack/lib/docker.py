import os
from pathlib import Path

import yaml


def get_docker_compose_content(path: str):
    return yaml.safe_load(Path(path).resolve().read_text())


def merge_docker_compose(destination: str, source: str):
    if not os.path.exists(source):
        return

    dest_content = {"version": None, "services": {}}
    if os.path.exists(destination):
        dest_content = get_docker_compose_content(destination)

    source_content = get_docker_compose_content(source)
    dest_content["services"].update(source_content["services"])
    dest_content["version"] = source_content["version"]

    with open(destination, "w") as destination_h:
        yaml.safe_dump(dest_content, destination_h)
