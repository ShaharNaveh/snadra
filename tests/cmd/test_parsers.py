"""
Testing for the functions and classes that are in:
    snadra/commands/__init__.py
"""
import pytest

from _snadra.cmd.parsers import dispatch_line, parse_line


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
    @pytest.mark.asyncio
    async def test_dispatch_line_empty(self, line, commands):
        result = await dispatch_line(line, commands=commands)
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
    def test_parse_line_empty(self, line):
        result = parse_line(line)
        assert result is None

    @pytest.mark.parametrize(
        "line, expected",
        [
            ("command", ["command"]),
            ("command ", ["command"]),  # Space at the end of the command
            (" command", ["command"]),  # Space at the beginning of the command
            (" command ", ["command"]),  # Space at the end and at the beginning
            ("command -f 1", ["command", "-f", "1"]),
            ("command --flag 1", ["command", "--flag", "1"]),
            ("command --flag  1", ["command", "--flag", "1"]),  # Extra space
        ],
    )
    def test_parse_line(self, line, expected):
        result = parse_line(line)
        assert result == expected

    @pytest.mark.parametrize(
        "line",
        [
            "invalid_command",
            "INVALID_COMMAND",
            "_",
        ],
    )
    @pytest.mark.asyncio
    async def test_dispatch_line_invalid_keyword(self, capfd, line, commands):
        expected_out = "unknown command"
        expected_err = ""
        await dispatch_line(line, commands=commands)

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
    def test_parse_line_shlex_split(self, line):
        result = parse_line(line)
        assert result is None
