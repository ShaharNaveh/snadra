import pytest

from snadra._core.commands import Commands
from snadra._core.parsers import CommandParser


@pytest.fixture(scope="module")
def commands() -> "Commands":
    """
    Returns
    -------
    Commands
        A ``Commands`` instance.
    """
    return Commands()


@pytest.fixture(scope="module")
def command_parser() -> "CommandParser":
    """
    Returns
    -------
    CommandParser
        A ``CommandParser`` instance.
    """
    return CommandParser()
