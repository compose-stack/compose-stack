from pathlib import Path

import yaml


def get_all_components():
    return yaml.safe_load(
        Path(__file__ + "../../../../components.yml").resolve().read_text()
    )


def get_component(components, stack, component):
    search = [c for c in components["components"][stack] if c["name"] == component]
    if len(search) == 1:
        return search[0]
    return None
