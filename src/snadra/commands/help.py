from typing import TYPE_CHECKING

from rich import box as rich_box
from rich.table import Table as RichTable

import snadra._utils as snutils
from snadra.core.base import CommandDefinition, Commands, Complete, Parameter

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

    def run(self, args: "argparse.Namespace"):
        if args.topic:
            if args.topic in self.KEYWORDS:
                snutils.console.print(self.LONG_HELP)
            else:
                target_command = self._commands.get_command(args.topic)
                snutils.console.print(target_command.LONG_HELP)

        elif args:
            help_table = RichTable(title="Help menu", box=rich_box.SIMPLE)
            help_table.add_column("Command")
            help_table.add_column("Description")

            for keyword in self.available_keywords:
                if keyword in self.KEYWORDS:
                    command = self
                else:
                    command = self._commands.get_command(keyword)

                command_description = command.DESCRIPTION
                help_table.add_row(keyword, command_description)

            snutils.console.print(help_table)
