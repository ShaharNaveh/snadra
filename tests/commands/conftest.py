import pytest

from snadra.commands import CommandParser


@pytest.fixture()
def command_parser() -> "CommandParser":
    """
    Returns
    -------
    CommandParser
        A ``CommandParser`` parser instance.
    """
    return CommandParser()
