import os

import snadra
from snadra.commands import _gather_modules


def test_gather_modules():
    snadra_dir = os.path.dirname(snadra.__file__)
    commands_dir = os.path.join(snadra_dir, "commands")
    path = [commands_dir]

    expected = sorted(["exit", "help"])
    result = sorted([module.__name__ for module in _gather_modules(path)])

    assert expected == result
