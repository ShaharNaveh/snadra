from snadra.commands import CommandParser
import pytest

@pytest.fixture()
def command_parser() -> "CommandParser":
    """
    Returns
    -------
    CommandParser
        A ``CommandParser`` parser instance.
    """
    return CommandParser()
