import pytest

import snadra._utils as snutils
from snadra._core.base import Commands
from snadra._core.parsers import CommandParser


@pytest.fixture
def commands() -> "Commands":
    """
    Returns
    -------
    Commands
        A ``Commands`` instance.
    """
    core_commands_dir = snutils.get_core_commands_dir()
    return Commands(command_dirs=core_commands_dir)


@pytest.fixture()
def command_parser() -> "CommandParser":
    """
    Returns
    -------
    CommandParser
        A ``CommandParser`` instance.
    """
    return CommandParser()
