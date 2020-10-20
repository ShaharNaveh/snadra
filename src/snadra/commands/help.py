"""
The command `help`, for displaying help information about other commands
"""
import typing

from snadra.commands._base import CommandDefinition

if typing.TYPE_CHECKING:
    import argparse


class Command(CommandDefinition):
    """
    list all known commands and print their help message.
    """

    KEYWORDS = ["help"]
    HELP_TEXT = "list all known commands and print their help message"

    def run(self, args: typing.Optional["argparse.Namespace"] = None):
        pass
