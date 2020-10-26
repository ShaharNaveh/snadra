"""
Testing for the functions and classes that are in:
    snadra/commands/__init__.py
"""
import pytest

from snadra.commands import Commands
from snadra.commands.exit import Command as ExitCommand
from snadra.commands.help import Command as HelpCommand


class TestCommandParser:
    @pytest.mark.parametrize(
        "line",
        [
            "",
            " ",
            " " * 3,
            "\n",
            "\n" * 3,
            "\n ",
            "\n " * 3,
            " \n",
            " \n" * 3,
            " \n ",
            " \n " * 3,
        ],
    )
    def test_dispatch_line_empty(self, command_parser, line):
        result = command_parser.dispatch_line(line)
        assert result is None

    @pytest.mark.parametrize(
        "line",
        [
            "",
            " ",
            " " * 3,
            "\n",
            "\n" * 3,
            "\n ",
            "\n " * 3,
            " \n",
            " \n" * 3,
            " \n ",
            " \n " * 3,
        ],
    )
    def test__parse_line_empty(self, command_parser, line):
        result = command_parser._parse_line(line)
        assert result is None

    @pytest.mark.parametrize(
        "line, expected",
        [
            ("command", (["command"], "command")),
            ("command ", (["command"], "command")),  # Space at the end of the command
            (
                " command",  # Space at the beginning of the command
                (["command"], "command"),
            ),
            (
                " command ",  # Space at the end and at the beginning of the command
                (["command"], "command"),
            ),
            ("command -f 1", (["command", "-f", "1"], "command -f 1")),
            ("command --flag 1", (["command", "--flag", "1"], "command --flag 1")),
            (
                "command --flag  1",
                (["command", "--flag", "1"], "command --flag  1"),  # Extra space
            ),
        ],
    )
    def test__parse_line(self, command_parser, line, expected):
        result = command_parser._parse_line(line)
        assert result == expected

    @pytest.mark.parametrize(
        "line",
        [
            "'command",
            '"command',
        ],
    )
    def test__parse_line_shlex_split(self, command_parser, line):
        result = command_parser._parse_line(line)
        assert result is None

    @pytest.mark.parametrize("keyword", ["exit", "help", "quit"])
    def test_has_command_valid(self, command_parser, keyword):
        assert command_parser.has_command(keyword)

    @pytest.mark.parametrize(
        "keyword",
        [
            "not_a_valid_command",
            " exit",
            "help ",
            "\n",
            "",
            " ",
        ],
    )
    def test_has_command_invalid(self, command_parser, keyword):
        assert not command_parser.has_command(keyword)

    @pytest.mark.parametrize(
        "keyword, expected",
        [("exit", ExitCommand()), ("help", HelpCommand()), ("quit", ExitCommand())],
    )
    def test_get_command_valid(self, command_parser, keyword, expected):
        result = command_parser.get_command(keyword)
        assert result == expected

    @pytest.mark.parametrize(
        "keyword",
        [
            "not_a_valid_command",
            " exit",
            "help ",
            "\n",
            "",
            " ",
        ],
    )
    def test_get_command_invalid(self, command_parser, keyword):
        result = command_parser.get_command(keyword)
        assert result is None
