import os

from rich.console import Console

console = Console()


def get_commands_dir() -> str:
    """
    Get the path to the commands dir.
    """
    import snadra

    snadra_dir = os.path.dirname(snadra.__file__)
    return os.path.join(snadra_dir, "commands")
