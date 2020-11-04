from typing import TYPE_CHECKING

import snadra._utils as snutils
from snadra.core.base import CommandDefinition, Commands, Complete, Parameter

if TYPE_CHECKING:
    import argparse


class Command(CommandDefinition):
    """
    The command `help`, for displaying help information about other commands
    """

    _core_commands_keywords = Commands(
        command_dirs=snutils.get_core_commands_dir(), ignore="help"
    ).keywords
    _core_commands_keywords.add("help")
    available_keywords = sorted(_core_commands_keywords)

    KEYWORDS = {"help"}
    HELP_TEXT = "List all known commands and print their help message"
    ARGS = {"topic": Parameter(Complete.CHOICES, choices=available_keywords, nargs="?")}

    def run(self, args: "argparse.Namespace"):
        if args.topic:
            pass
        elif args:
            pass
