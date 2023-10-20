from compose_stack.lib.check_stack import check_stack
from compose_stack.lib.constants import COMPOSE_FOLDER, COMPOSE_TMP_FOLDER
from compose_stack.lib.docker import merge_docker_compose
from compose_stack.lib.files import (
    copy_folder,
    create_folder,
    delete_files,
    delete_folders,
    extract_archive,
    merge_gitignore,
)
from compose_stack.lib.initialise import initialise_component
from compose_stack.lib.repository import download_repository_code
from compose_stack.lib.console import console


def compose(
    backend: str = None,
    frontend: str = None,
    fullstack: str = None,
    todos: bool = False,
):
    delete_folders([COMPOSE_FOLDER])
    create_folder(COMPOSE_FOLDER)
    components = check_stack(backend, frontend, fullstack)

    for stack in components:
        component = components[stack]
        if not component:
            continue

        clean_component_files(stack)
        clean_component_tmp_files(stack)
        console.print(f'Download {stack}: {component["repository"]}')
        download_repository_code(component["repository"], stack, todos)
        stack_tmp_folder = get_stack_folder(stack, tmp=True)
        create_folder(stack_tmp_folder)
        extract_archive(f"{stack}.zip", stack_tmp_folder)

        component_name = get_component_name(component, todos)

        copy_folder(
            f"{stack_tmp_folder}/{component_name}",
            f"{COMPOSE_FOLDER}/",
            get_ignore_files(stack, component_name),
        )
        merge_gitignore(
            f"{COMPOSE_FOLDER}/.gitignore",
            f"{stack_tmp_folder}/{component_name}/.gitignore",
        )
        for env in ["dev", "test", "prod"]:
            merge_docker_compose(
                f"{COMPOSE_FOLDER}/docker-compose.{env}.yml",
                f"{stack_tmp_folder}/{component_name}/docker-compose.{env}.yml",
            )

            initialise_component(stack, env)

        clean_component_tmp_files(stack)


def clean_component_tmp_files(stack: str):
    zip_file = f"{stack}.zip"
    stack_tmp_folder = get_stack_folder(stack, True)

    files = [zip_file]
    folders = [stack_tmp_folder]

    delete_files(files)
    delete_folders(folders)


def clean_component_files(stack: str):
    zip_file = f"{stack}.zip"
    stack_folder = get_stack_folder(stack)
    stack_tmp_folder = get_stack_folder(stack, True)

    files = [zip_file]
    folders = [stack_folder, stack_tmp_folder]

    delete_files(files)
    delete_folders(folders)


def get_stack_folder(stack: str, tmp: bool = False):
    if tmp:
        return f"{COMPOSE_TMP_FOLDER}/{stack}"
    return f"{COMPOSE_FOLDER}/{stack}"


def get_component_name(component, todos: bool = False):
    suffix = "-todos" if todos else "-main"
    return f"{component['name']}{suffix}"


def get_ignore_files(stack, component_name):
    root_folder = f"{get_stack_folder(stack, True)}/{component_name}"

    def ignore_files(folder, files):
        if folder != root_folder:
            return []
        return [
            "compose-stack.yml",
            "docker-compose.dev.yml",
            "docker-compose.test.yml",
            "docker-compose.prod.yml",
            ".gitignore",
            "README.md",
        ]

    return ignore_files
