import os
from pathlib import Path
from typing import Literal

import yaml

from compose_stack.lib.console import console
from compose_stack.lib.files import copy_file, create_folder

from .constants import COMPOSE_FOLDER

Command = Literal["cp", "mkdir", "chmod", "print"]


def initialise_component(stack: str, env: str):
    folder = in_compose(f"{stack}_docker")
    if not os.path.exists(folder):
        return

    env_file = f"{folder}/initialise_{env}.yml"
    if not os.path.exists(env_file):
        return

    ops = yaml.safe_load(Path(env_file).resolve().read_text())
    console.print(f"[cyan]{ops['intro']}[/cyan]")
    for operation in ops["operations"]:
        console.print(f"\t{operation['name']} ({env})")
        for command_dict in operation["commands"]:
            for command in command_dict:
                execute_command(command, command_dict[command])


def execute_command(command: Command, payload):
    if command == "cp":
        copy_file(in_compose(payload[0]), in_compose(payload[1]))
    if command == "mkdir":
        create_folder(in_compose(payload))
    if command == "chmod":
        os.chmod(in_compose(payload[1]), int(payload[0], 8))
    if command == "print":
        print_command(payload)


def in_compose(path: str):
    return f"{COMPOSE_FOLDER}/{path}"


def print_command(payload):
    color = ("", "")
    if len(payload) == 2:
        options = payload[1]
    if options.get("color"):
        color = (f"[{options['color']}]", f"[/{options['color']}]")
    console.print(f"\t\t{color[0]}{payload[0]}{color[1]}")
