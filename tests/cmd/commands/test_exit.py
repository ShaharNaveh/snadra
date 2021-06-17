import argparse

import pytest

import _snadra.cmd.commands.exit as module


@pytest.fixture
def command():
    """
    Return the tested command.
    """
    return module.Command()


@pytest.mark.asyncio
class TestExitCommand:
    async def test_run(self, command):
        args = argparse.Namespace()

        with pytest.raises(EOFError, match="Got an exit signal"):
            await command.run(args)
