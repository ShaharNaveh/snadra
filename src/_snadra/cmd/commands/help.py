from typing import TYPE_CHECKING

from rich import box as rich_box
from rich.table import Table as RichTable

from _snadra.cmd import SnadraConsole
from _snadra.cmd.base import Complete, Parameter
from _snadra.cmd.commands import Commands
from _snadra.cmd.utils import CommandMeta

if TYPE_CHECKING:
    import argparse


class Command(CommandMeta):
    """
    The command `help`, for displaying help information about other commands.
    """

    keyword = "help"
    aliases = {"HELP"}
    description = "List all known commands and print their help message"
    long_help = "THE LONG HELP MESSAGE OF 'help'"

    # Skipping "help" so we won't make a circular import
    __commands = Commands(skip={"help"})
    available_keywords = __commands.keywords.union({keyword}).union(aliases)

    arguments = {
        "topic": Parameter(
            Complete.CHOICES,
            choices=sorted(available_keywords),
            nargs="?",
        )
    }

    async def run(self, args: "argparse.Namespace") -> None:
        """
        Show the help.

        Parameters
        ----------
        args : :class:`argparse.Namespace`
            The arguments for the command.
        """
        if args.topic:
            if args.topic in self.available_keywords:
                SnadraConsole().print(self.long_help)
            else:
                # Here we are counting on "argparse" choices for validation.
                target_command = self.__commands.get_command(args.topic)
                SnadraConsole().print(target_command.long_help)  # type: ignore

        elif args:
            help_table = RichTable(title="Help menu", box=rich_box.SIMPLE)
            help_table.add_column("Command")
            help_table.add_column("Description")

            for keyword in self.available_keywords:
                if keyword == self.keyword or keyword in self.aliases:
                    command_description = self.description
                else:
                    command_description = self.__commands.get_command(keyword).description  # type: ignore # noqa: E501

                help_table.add_row(keyword, command_description)

            SnadraConsole().print(help_table)
