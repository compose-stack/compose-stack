import typer

from compose_stack.commands import compose as compose_command
from compose_stack.commands import ls as ls_command
from compose_stack.commands import test as test_command
from compose_stack.lib.console import console


app = typer.Typer()


@app.command()
def compose(
    backend: str = None,
    frontend: str = None,
    fullstack: str = None,
    todos: bool = False,
):
    compose_command.compose(backend, frontend, fullstack, todos)
    """
    try:
        compose_command.compose(backend, frontend, fullstack)
    except Exception as e:
        console.print("[red]An error occurred:[/red]")
        console.print(str(e))
        exit(1)
    """


@app.command()
def ls():
    ls_command.list_components()


@app.command()
def test():
    test_command.test_application()


def main():
    app()


if __name__ == "__main__":
    app()
