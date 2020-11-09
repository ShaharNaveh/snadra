from typing import TYPE_CHECKING

from rich import box as rich_box
from rich.table import Table as RichTable

from snadra._core.base import CommandDefinition, Complete, Parameter
from snadra._core.commands import Commands
import snadra._utils as snutils

if TYPE_CHECKING:
    import argparse


class Command(CommandDefinition):
    """
    The command `help`, for displaying help information about other commands.
    """

    _commands = Commands(
        command_dirs=snutils.get_core_commands_dir(),
        ignore="help",  # ignoring help so we don't create a circular dependency
    )
    _core_commands_keywords = _commands.keywords
    _core_commands_keywords.add("help")
    available_keywords = sorted(_core_commands_keywords)

    KEYWORDS = {"help"}
    DESCRIPTION = "List all known commands and print their help message"
    LONG_HELP = "THE LONG HELP MESSAGE OF 'help'"

    # TODO: Get rid of this 'choices' and make better handling and
    # display better information about the commands and how to use the help command.
    ARGS = {"topic": Parameter(Complete.CHOICES, choices=available_keywords, nargs="?")}

    def run(self, args: "argparse.Namespace") -> None:
        """
        Show the help.

        Parameters
        ----------
        args : :class:`argparse.Namespace`
            The arguments for the command.
        """
        if args.topic:
            if args.topic in self.KEYWORDS:
                snutils.console.print(self.LONG_HELP)
            else:
                # Here we are counting on "argparse" choices for validation.
                target_command = self._commands.get_command(args.topic)
                snutils.console.print(target_command.LONG_HELP)  # type: ignore

        elif args:
            help_table = RichTable(title="Help menu", box=rich_box.SIMPLE)
            help_table.add_column("Command")
            help_table.add_column("Description")

            for keyword in self.available_keywords:
                if keyword in self.KEYWORDS:
                    command_description = self.DESCRIPTION
                else:
                    command_description = self._commands.get_command(keyword).DESCRIPTION  # type: ignore # noqa: E501

                help_table.add_row(keyword, command_description)

            snutils.console.print(help_table)
