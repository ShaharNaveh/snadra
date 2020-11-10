import os
import pathlib

from rich.console import Console

console = Console()


def get_core_commands_dir() -> str:
    """
    Get the path to the commands dir.
    """
    import snadra

    snadra_dir = pathlib.Path(snadra.__file__)
    return os.path.join(snadra_dir, "_core", "commands")
