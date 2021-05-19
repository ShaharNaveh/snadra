"""
Testing general things about the commands
"""
from typing import List

from hypothesis import assume, given
import hypothesis.strategies as st
import pytest

from snadra._core.commands import Commands


class TestCommands:
    def test_keywords(self):
        """
        Test if all the expected keywords of the commands, are in `Commands.keywords`.
        """
        commands = Commands()
        expected = {"exit", "help", "quit"}
        result = commands.keywords

        assert result == expected

    @pytest.mark.parametrize("keyword", ["exit", "help", "quit"])
    def test_is_valid_keyword_valid(self, keyword):
        commands = Commands()
        assert commands.is_valid_keyword(keyword)

    @given(keyword=st.text())
    def test_is_valid_keyword_invalid(self, keyword):
        commands = Commands()
        assume(keyword not in commands.keywords)
        assert not commands.is_valid_keyword(keyword)

    def test_no_duplicate_keywords(self):
        """
        Check if two commands or more are sharing the same keyword.
        """
        commands = Commands()
        result: List[str] = []
        seen_commands = set()
        for command_keyword in commands.keywords:
            command = commands.get_command(command_keyword)
            if command in seen_commands:
                continue
            seen_commands.add(command)
            for keyword in command.keywords:
                result.append(keyword)

        expected = list(set(result))
        assert sorted(result) == sorted(expected)

    @given(keyword=st.text())
    def test_get_command_invalid(self, keyword):
        commands = Commands()
        assume(keyword not in commands.keywords)
        result = commands.get_command(keyword)
        assert result is None
