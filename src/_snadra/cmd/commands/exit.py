"""
The command to exit snadra.
"""
from typing import TYPE_CHECKING

from _snadra.cmd.utils import CommandMeta

if TYPE_CHECKING:
    import argparse


class Command(CommandMeta):
    """
    Help message for "exit".
    """

    keyword = "exit"
    aliases = {"quit"}
    description = "Exit the console"
    long_help = "LONG HELP FOR EXIT COMMAND"

    async def run(self, args: "argparse.Namespace") -> None:
        """
        Exit `snadra`.

        Parameters
        ----------
        args : :class:`argparse.Namespace`
            The arguments for the command.
        """
        raise EOFError("Got an exit signal")
