import pytest

from snadra.core.base import Commands
from snadra.core.parsers import CommandParser


@pytest.fixture
def commands() -> "Commands":
    """
    Returns
    -------
    Commands
        A ``Commands`` instance.
    """
    return Commands()


@pytest.fixture()
def command_parser() -> "CommandParser":
    """
    Returns
    -------
    CommandParser
        A ``CommandParser`` instance.
    """
    return CommandParser()
