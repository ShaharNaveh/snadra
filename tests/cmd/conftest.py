import pytest

from _snadra.cmd.commands import Commands


@pytest.fixture(scope="class")
def commands():
    return Commands()
