import os

import pytest

import snadra
from snadra.commands import _get_modules, find_modules


#@pytest.fixture

def commands_dir() -> str:
    snadra_dir = os.path.dirname(snadra.__file__)
    return os.path.join(snadra_dir, "commands")


def test_get_modules(commands_dir):
    path = [commands_dir]

    expected = sorted(["exit", "help"])
    result = sorted([module.__name__ for module in _get_modules(path)])

    assert expected == result


@pytest.mark.parametrize("dir_path, to_ignore, expected_modules", [
    (commands_dir(), None, ["_base", "exit", "help"]),


    ])
def test_find_modules(dir_path, to_ignore, expected_modules):
    path = [dir_path]
    expected = sorted(expected_modules)
    result = sorted([module.name for module in find_modules(path)])

