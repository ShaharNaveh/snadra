"""
foo
"""
import typing

from snadra.commands._base import CommandDefinition

if typing.TYPE_CHECKING:
    import argparse


class Command(CommandDefinition):
    """
    Help message for "exit"
    """

    PROG = "exit"

    def run(self, args: typing.Optional["argparse.Namespace"] = None):
        raise EOFError("Got an exit signal")
