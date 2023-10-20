from compose_stack.lib.components import get_all_components
from compose_stack.lib.console import console


def list_components():
    components = get_all_components()
    list_stack_components(components, "backend")
    list_stack_components(components, "frontend")
    list_stack_components(components, "fullstack")


def list_stack_components(components, stack):
    console.print(f"[bold cyan]{stack}:[/bold cyan]")
    for component in components["components"].get(stack, []):
        console.print(f"\t- {component['name']}")
