import pathlib

from rich.console import Console

SNADRA_DIR = pathlib.Path(__file__).parent.resolve()
console = Console()


def relative_to_root_dir(path):
    """
    foo bar baz.
    """
    pass
