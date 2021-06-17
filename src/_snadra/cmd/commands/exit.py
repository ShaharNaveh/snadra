"""
The command to exit snadra.
"""
from typing import TYPE_CHECKING

from _snadra.cmd.base import Complete, Parameter
from _snadra.cmd.utils import CommandMeta, console

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

    arguments = {
        "-y,--yes": Parameter(
            complete=Complete.NONE, action="store_true", help="Confirm to exit"
        )
    }

    async def run(self, args: "argparse.Namespace") -> None:
        """
        Exit `snadra`.

        Parameters
        ----------
        args : :class:`argparse.Namespace`
            The arguments for the command.
        """
        if not args.yes:
            console.log("[red]Error[/red]: Exit not confirmed (use '--yes')")
            return

        raise EOFError("Got an exit signal")
