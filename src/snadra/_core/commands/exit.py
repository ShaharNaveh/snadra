"""
The command to exit snadra.
"""
from typing import TYPE_CHECKING

from snadra._core.base import CommandDefinition, Complete, Parameter
import snadra._utils as snutils

if TYPE_CHECKING:
    import argparse


class Command(CommandDefinition):
    """
    Help message for "exit"
    """

    KEYWORDS = {"exit", "quit"}
    DESCRIPTION = "Exit the console"
    LONG_HELP = "LONG HELP FOR EXIT COMMAND"

    ARGS = {
        "-y,--yes": Parameter(
            complete=Complete.NONE, action="store_true", help="Confirm to exit"
        )
    }

    def run(self, args: "argparse.Namespace") -> None:
        """
        Exit `snadra`.

        Parameters
        ----------
        args : :class:`argparse.Namespace`
            The arguments for the command.
        """
        if not args.yes:
            snutils.console.log("[red]Error[/red]: Exit not confirmed (use '--yes')")
            return

        raise EOFError("Got an exit signal")
