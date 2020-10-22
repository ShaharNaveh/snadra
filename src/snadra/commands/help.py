"""
foo bar baz
"""
from typing import TYPE_CHECKING, Optional

# import snadra
from snadra.commands._base import CommandDefinition

# Complete, Parameter

if TYPE_CHECKING:
    import argparse


class Command(CommandDefinition):
    """
    The command `help`, for displaying help information about other commands
    """

    KEYWORDS = ["help"]
    HELP_TEXT = "list all known commands and print their help message"
    # ARGS = {"topic": Parameter(Complete.CHOICES, choices="A")}

    def run(self, args: Optional["argparse.Namespace"] = None):
        """
        foo bar baz
        """
        pass
