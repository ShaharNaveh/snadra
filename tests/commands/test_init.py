"""
Testing for the functions and classes that are in:
    snadra/commands/__init__.py
"""
import pytest

from snadra.commands import CommandParser, find_modules


@pytest.fixture(scope="function")
def command_parser() -> "CommandParser":
    """
    Returns a ``CommandParser`` instance.
    """
    return CommandParser()


@pytest.mark.parametrize(
    "to_ignore, expected",
    [
        (None, ["foo", "bar", "baz"]),
        ({}, ["foo", "bar", "baz"]),
        ({"foo"}, ["bar", "baz"]),
        ({"foo", "bar"}, ["baz"]),
        ({"foo", "bar", "baz"}, []),
    ],
)
def test_find_modules(tmpdir, to_ignore, expected):
    commands_dir = tmpdir.mkdir("commands")
    files = {"foo", "bar", "baz", "__init__"}

    for file_name in files:
        commands_dir.join(f"{file_name}.py").write("")

    path = [str(commands_dir)]

    result = [module.name for module in find_modules(path, to_ignore=to_ignore)]

    assert sorted(result) == sorted(expected)


class TestCommandParser:
    def test_loaded_modules(self, command_parser):
        expected = ["exit", "help"]
        loaded_modules = command_parser._loaded_modules
        result = [module.__name__ for module in loaded_modules]
        assert sorted(result) == sorted(expected)

    @pytest.mark.parametrize(
        "line",
        [
            "",
            " ",
            " " * 3,
            "\n",
            "\n" * 3,
        ],
    )
    def test_dispatch_line_empty(self, command_parser, line):
        result = command_parser.dispatch_line(line)
        assert result is None
