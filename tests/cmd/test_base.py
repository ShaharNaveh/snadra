"""
Testing general things about the commands
"""
from hypothesis import assume, given
import hypothesis.strategies as st
import pytest


class TestCommands:
    def test_keywords(self, commands):
        """
        Test if all the expected keywords of the commands, are in `Commands.keywords`.
        """
        expected = {"exit", "help", "workspace"}
        result = commands.keywords

        assert result == expected

    def test_aliases(self, commands):
        """
        Test if all the expected aliases of the commands, are in `Commands.keywords`.
        """
        expected = {"HELP", "quit", "workspaces"}
        result = commands.aliases

        assert result == expected

    @pytest.mark.parametrize("keyword", ["exit", "help", "quit"])
    def test_is_valid_keyword_valid(self, keyword, commands):
        assert commands.is_valid_keyword(keyword)

    @given(keyword=st.text())
    def test_is_valid_keyword_invalid(self, keyword, commands):
        assume(keyword not in commands.all_keywords)
        assert not commands.is_valid_keyword(keyword)

    def test_no_duplicate_keywords_and_aliases(self, commands):
        """
        Check if two commands or more are sharing the same keyword or alias.
        """
        result = []
        seen_commands = set()

        for keyword in commands.all_keywords:
            command = commands.get_command(keyword)
            if command in seen_commands:
                continue
            seen_commands.add(command)
            result.append(command.keyword)
            for alias in command.aliases:
                result.append(alias)

        expected = list(set(result))
        assert sorted(result) == sorted(expected)

    @given(keyword=st.text())
    def test_get_command_invalid(self, keyword, commands):
        assume(keyword not in commands.all_keywords)
        result = commands.get_command(keyword)
        assert result is None
