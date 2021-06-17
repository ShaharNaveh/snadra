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
    async def test_confirm(self, capfd, command):
        args = argparse.Namespace(yes=False)
        expected_err = ""
        expected_out = "Exit not confirmed"

        await command.run(args)

        captured = capfd.readouterr()

        assert expected_out in captured.out
        assert expected_err == captured.err

    async def test_run(self, command):
        args = argparse.Namespace(yes=False)
        assert await command.run(args) is None

    async def test_run_confirm(self, command):
        args = argparse.Namespace(yes=True)

        with pytest.raises(EOFError, match="Got an exit signal"):
            await command.run(args)
