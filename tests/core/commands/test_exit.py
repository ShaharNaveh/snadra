import argparse

import pytest

import snadra._core.commands.exit as module


@pytest.fixture
def command():
    """
    Return the tested command.
    """
    return module.Command()


class TestExitCommand:
    def test_confirm(self, capfd, command):
        args = argparse.Namespace(yes=False)
        expected_err = ""
        expected_out = "Exit not confirmed"

        command.run(args)

        captured = capfd.readouterr()

        assert expected_out in captured.out
        assert expected_err == captured.err

    def test_run(self, command):
        args = argparse.Namespace(yes=False)
        assert command.run(args) is None

    def test_run_confirm(self, command):
        args = argparse.Namespace(yes=True)

        with pytest.raises(EOFError, match="Got an exit signal"):
            command.run(args)
