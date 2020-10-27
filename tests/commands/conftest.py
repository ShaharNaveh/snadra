import pytest

from snadra.commands import CommandParser, Commands


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
