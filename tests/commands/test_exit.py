import argparse

import pytest

import snadra.commands.exit as module


def test_run():
    command = module.Command()
    assert command.run() is None


def test_run_confirm():
    command = module.Command()
    args = argparse.Namespace(yes=True)
    with pytest.raises(EOFError, match="Got an exit signal"):
        command.run(args)
