"""
foo
"""
from typing import TYPE_CHECKING, Optional

from snadra.commands._base import CommandDefinition, Complete, Parameter

if TYPE_CHECKING:
    import argparse


class Command(CommandDefinition):
    """
    Help message for "exit"
    """

    KEYWORDS = ["exit", "quit"]
    HELP_TEXT = "Exit the console"

    ARGS = {
        "-y,--yes": Parameter(
            complete=Complete.NONE, action="store_true", help="Confirm to exit"
        )
    }

    def run(self, args: Optional["argparse.Namespace"] = None):
        """
        Exit `snadra`.
        """
        if args is None or not args.yes:
            # TODO: Display some message here, to tell the user how to exit
            return

        raise EOFError("Got an exit signal")
