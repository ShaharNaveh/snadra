import pytest

from _snadra.cmd.base import Commands


@pytest.fixture(scope="class")
def commands():
    return Commands()
