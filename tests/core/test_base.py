"""
Testing general things about the commands
"""
from typing import List

from hypothesis import assume, given
import hypothesis.strategies as st
import pytest

from snadra._core.commands import Commands
from snadra._core.commands.exit import Command as ExitCommand
from snadra._core.commands.help import Command as HelpCommand


class TestCommands:
    @pytest.mark.parametrize(
        "ignore, expected",
        [
            (None, ["foo", "bar", "baz"]),
            ({}, ["foo", "bar", "baz"]),
            ({"foo"}, ["bar", "baz"]),
            ({"foo", "bar"}, ["baz"]),
            ({"foo", "bar", "baz"}, []),
        ],
    )
    def test__find_modules(self, tmpdir, ignore, expected):
        commands_dir = tmpdir.mkdir("commands")
        files = {"foo", "bar", "baz", "__init__"}

        for file_name in files:
            commands_dir.join(f"{file_name}.py").write("")

        path = [str(commands_dir)]

        result = [module.name for module in Commands._find_modules(path, ignore=ignore)]

        assert sorted(result) == sorted(expected)

    def test_keywords(self, commands):
        """
        Test if all the expected keywords of the commands, are in `Commands.keywords`.
        """
        expected = {"exit", "help", "quit"}
        result = commands.keywords

        assert result == expected

    @pytest.mark.parametrize("keyword", ["exit", "help", "quit"])
    def test_is_valid_keyword_valid(self, commands, keyword):
        assert commands.is_valid_keyword(keyword)


    @given(keyword=st.text())
    def test_is_valid_keyword_invalid(self, commands, keyword):
        assume(keyword not in commands.keywords)
        assert not commands.is_valid_keyword(keyword)

    def test_no_duplicate_keywords(self, commands):
        """
        Check if two commands or more are sharing the same keyword.
        """
        result: List[str] = []
        seen_commands = set()
        for command_keyword in commands.keywords:
            command = commands.get_command(command_keyword)
            if command in seen_commands:
                continue
            seen_commands.add(command)
            for keyword in command.KEYWORDS:
                result.append(keyword)

        expected = list(set(result))
        assert sorted(result) == sorted(expected)

    @pytest.mark.parametrize(
        "keyword, expected",
        [
            ("help", HelpCommand()),
            ("quit", ExitCommand()),
            ("exit", ExitCommand()),
        ],
    )
    def test_get_command_valid(self, commands, keyword, expected):
        result = commands.get_command(keyword)
        assert result == expected

    @given(keyword=st.text())
    def test_get_command_invalid(self, commands, keyword):
        assume(keyword not in commands.keywords)
        result = commands.get_command(keyword)
        assert result is None
