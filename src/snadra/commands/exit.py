"""
foo
"""
from typing import TYPE_CHECKING, Optional

from snadra.commands._base import CommandDefinition

if TYPE_CHECKING:
    import argparse


class Command(CommandDefinition):
    """
    Help message for "exit"
    """

    KEYWORDS = ["exit", "quit"]
    HELP_TEXT = "Exit the console"

    def run(self, args: Optional["argparse.Namespace"] = None):
        raise EOFError("Got an exit signal")
