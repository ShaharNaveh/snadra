"""
foo bar baz
"""
import pkgutil
import shlex
import typing

from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import InMemoryHistory

import snadra.utils as utils

if typing.TYPE_CHECKING:
    from snadra.commands._base import CommandDefinition

logger = utils.get_logger(__name__)


class CommandParser:
    """
    foo bar baz
    """

    def __init__(self) -> None:
        """
        foo bar baz
        """
        self.commands: typing.List["CommandDefinition"] = []
        for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
            if module_name == "_base":
                continue
            self.commands.append(
                loader.find_module(module_name).load_module(module_name).Command()
            )

        logger.debug(f"Registered commands: {self.commands}")
        self.prompt: "PromptSession" = None

    def setup_prompt(self):
        """
        foo bar baz
        """
        history = InMemoryHistory()
        auto_suggest = AutoSuggestFromHistory()
        self.prompt = PromptSession(
            "snadra > ",
            auto_suggest=auto_suggest,
            history=history,
        )

    def run(self):
        self.running = True
        while self.running:
            try:
                line = self.prompt.prompt().strip()
                if line == "":
                    continue
                self.dispatch_line(line)
            except EOFError:
                self.running = False
            except KeyboardInterrupt:
                continue

    def dispatch_line(self, line: str, prog_name: typing.Optional = None):
        """
        foo bar baz
        """
        line = line.strip()
        if line == "":
            return

        try:
            argv = shlex.split(line)
        except ValueError as err:
            logger.error(f"Error: {err.args[0]}")
            return

        line = f"{argv[0]} ".join(line.split(f"{argv[0]} "))

        for command in self.commands:
            if command.PROG == argv[0]:
                break
        else:
            logger.error(f"Erro: {argv[0]}: unknown command")
            return

        args = argv[1:]
        args = [a.encode("utf-8").decode("unicode_escape") for a in args]

        try:
            if prog_name:
                temp_name = command.parser.prog
                command.parser.prog = prog_name
                prog_name = temp_name

            if command.parser:
                args = command.parser.parse_args(args)
            else:
                args = line

            command.run(args)

            if prog_name:
                command.parser.prog = prog_name

        except SystemExit:
            logger.error("A")
            return
