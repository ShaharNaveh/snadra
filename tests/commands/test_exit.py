import pytest

import snadra.commands.exit as module


def test_run():
    command = module.Command()
    with pytest.raises(EOFError, match="Got an exit signal"):
        command.run()
