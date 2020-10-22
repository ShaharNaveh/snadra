import os

import pytest

import snadra
from snadra.commands import find_modules

_snadra_dir = os.path.dirname(snadra.__file__)
COMMANDS_DIR = os.path.join(_snadra_dir, "commands")


# TODO: make this test scale better.
@pytest.mark.parametrize(
    "dir_path, to_ignore, expected_modules",
    [
        (COMMANDS_DIR, None, ["exit", "help", "_base"]),
        (COMMANDS_DIR, {"_base"}, ["exit", "help"]),
    ],
)
def test_find_modules(dir_path, to_ignore, expected_modules):
    path = [dir_path]
    expected = sorted(expected_modules)
    result = sorted([module.name for module in find_modules(path, to_ignore=to_ignore)])

    assert result == expected
