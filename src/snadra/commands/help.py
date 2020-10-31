"""
foo bar baz
"""
from typing import TYPE_CHECKING, Optional

import snadra._utils as snutils

# import snadra
from snadra.core.base import CommandDefinition, Commands, Complete, Parameter

# Complete, Parameter

if TYPE_CHECKING:
    import argparse


# _c = Commands().keywords
class Command(CommandDefinition):
    """
    The command `help`, for displaying help information about other commands
    """

    KEYWORDS = {"help"}
    HELP_TEXT = "List all known commands and print their help message"
    ARGS = {
        "topic": Parameter(
            Complete.CHOICES, choices={"help", "quit", "exit"}, nargs="?"
        )
    }

    def run(self, args: Optional["argparse.Namespace"] = None):
        """
        foo bar baz
        """
        snutils.console.log(args, log_locals=True)
