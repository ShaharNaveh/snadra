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
    ARGS = {"topic": Parameter(Complete.CHOICES, choices=available_keywords, nargs="?")}

    # _commands_dict = _commands._commands_dict

    def run(self, args: "argparse.Namespace"):
        if args.topic:
            if args.topic in self.KEYWORDS:
                snutils.console.print(self.LONG_HELP)
            else:
                target_command = self._commands.get_command(args.topic)
                snutils.console.print(target_command.LONG_HELP)

        elif args:
            snutils.console.print("Printing the entire commands table")
