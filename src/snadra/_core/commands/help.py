from typing import TYPE_CHECKING, Set

from rich import box as rich_box
from rich.table import Table as RichTable

from snadra._core.base import Complete, Parameter
from snadra._core.commands import Commands
import snadra._utils as snutils
from snadra._utils import CommandMeta

if TYPE_CHECKING:
    import argparse


def _all_available_keywords(commands: Commands, help_keywords: Set[str]) -> Set[str]:
    """
    All the available keywords, of the core commands.

    Parameters
    ----------
    commands : snadra._core.commands.Commands
        Commands objecs.
    help_keywords : set of str
        Keywords of the `help` command.

    Returns
    -------
    set of str
        All the available, core command's keywords.

    See Also
    --------
    snadra._core.commands.Commands
    """
    commands_keywords = commands.keywords
    all_available_keywords = commands_keywords.union(help_keywords)
    return all_available_keywords


class Command(CommandMeta):
    """
    The command `help`, for displaying help information about other commands.
    """

    # TODO: Add tests

    keywords = {"help"}
    description = "List all known commands and print their help message"
    long_help = "THE LONG HELP MESSAGE OF 'help'"

    # TODO: Get rid of this 'choices' and make better handling and
    # display better information about the commands and how to use the help command.
    _core_commands = Commands(
        skip={
            "__init__",
            "help",  # Skipping "help" so we won't make a circular import
        }
    )
    _available_keywords = sorted(
        _all_available_keywords(commands=_core_commands, help_keywords=keywords)
    )
    arguments = {
        "topic": Parameter(
            Complete.CHOICES,
            choices=_available_keywords,
            nargs="?",
        )
    }

    def run(self, args: "argparse.Namespace") -> None:
        """
        Show the help.

        Parameters
        ----------
        args : :class:`argparse.Namespace`
            The arguments for the command.
        """
        if args.topic:
            if args.topic in self.keywords:
                snutils.console.print(self.long_help)
            else:
                # Here we are counting on "argparse" choices for validation.
                target_command = self._core_commands.get_command(args.topic)
                snutils.console.print(target_command.long_help)  # type: ignore

        elif args:
            help_table = RichTable(title="Help menu", box=rich_box.SIMPLE)
            help_table.add_column("Command")
            help_table.add_column("Description")

            for keyword in self._available_keywords:
                if keyword in self.keywords:
                    command_description = self.description
                else:
                    command_description = self._core_commands.get_command(keyword).description  # type: ignore # noqa: E501

                help_table.add_row(keyword, command_description)

            snutils.console.print(help_table)
