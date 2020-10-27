"""
Testing for the functions and classes that are in:
    snadra/commands/__init__.py
"""
import pytest


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
            "invalid_command",
            "INVALID_COMMAND",
            "_",
        ],
    )
    def test_dispatch_line_invalid_keyword(self, capfd, command_parser, line):
        expected_out = "unknown command"
        expected_err = ""
        command_parser.dispatch_line(line)

        captured = capfd.readouterr()
        captured_out, captured_err = captured.out, captured.err

        assert expected_out in captured_out
        assert f"'{line}'" in captured_out

        assert captured_err == expected_err


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
