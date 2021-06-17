import pytest

from _snadra.cmd.commands import Commands
from _snadra.cmd.parsers import CommandParser


@pytest.fixture(scope="class")
def commands():
    return Commands()


@pytest.fixture(scope="class")
def command_parser():
    return CommandParser()
