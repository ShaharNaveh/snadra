"""
Testing general things about the commands
"""
from typing import List

from hypothesis import assume, given
import hypothesis.strategies as st
import pytest


class TestCommands:
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

    @given(keyword=st.text())
    def test_get_command_invalid(self, commands, keyword):
        assume(keyword not in commands.keywords)
        result = commands.get_command(keyword)
        assert result is None
