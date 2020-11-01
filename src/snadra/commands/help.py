"""
foo bar baz
"""
from typing import TYPE_CHECKING, Optional

import snadra._utils as snutils

# from snadra.core.base import Commands
from snadra.core.base import CommandDefinition, Complete, Parameter

if TYPE_CHECKING:
    import argparse


class Command(CommandDefinition):
    """
    The command `help`, for displaying help information about other commands
    """

    KEYWORDS = {"help"}
    HELP_TEXT = "List all known commands and print their help message"
    # TODO: Fix this, so the choises will be genereted, and not just debug from 2AM.
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
