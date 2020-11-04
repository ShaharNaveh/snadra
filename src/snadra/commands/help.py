"""
foo bar baz
"""
from typing import TYPE_CHECKING

import snadra._utils as snutils
from snadra.core.base import CommandDefinition, Commands, Complete, Parameter

if TYPE_CHECKING:
    import argparse

# TODO: Have a function to collect all the keywords


class Command(CommandDefinition):
    """
    The command `help`, for displaying help information about other commands
    """

    _core_commands_keywords = Commands(
        command_dirs=snutils.get_core_commands_dir(), ignore="help"
    ).keywords
    _core_commands_keywords.add("help")

    KEYWORDS = {"help"}
    HELP_TEXT = "List all known commands and print their help message"
    # TODO: Fix this, so the choises will be genereted, and not just debug from 2AM.
    ARGS = {
        "topic": Parameter(Complete.CHOICES, choices=_core_commands_keywords, nargs="?")
    }

    def run(self, args: "argparse.Namespace"):
        """
        foo bar baz
        """
        pass
