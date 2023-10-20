from compose_stack.lib.components import get_component, get_all_components
from compose_stack.lib.console import console
from compose_stack.lib.exceptions import ComponentDoesNotExists, InvalidStackException


def check_stack(backend: str = None, frontend: str = None, fullstack: str = None):
    if not backend and not frontend and not fullstack:
        console.print("You need to select at least one component.")
        raise InvalidStackException()

    components = {
        "backend": None,
        "frontend": None,
        "fullstack": None,
    }

    all_components = get_all_components()
    if backend:
        components["backend"] = get_component(all_components, "backend", backend)
        if not components["backend"]:
            raise ComponentDoesNotExists(
                f"Backend component {backend} does not exists."
            )
    if frontend:
        components["frontend"] = get_component(all_components, "frontend", frontend)
        if not components["frontend"]:
            raise ComponentDoesNotExists(
                f"Frontend component {frontend} does not exists."
            )
    if fullstack:
        components["fullstack"] = get_component(all_components, "fullstack", fullstack)
        if not components["fullstack"]:
            raise ComponentDoesNotExists(
                f"Fullstack component {fullstack} does not exists."
            )

    return components
