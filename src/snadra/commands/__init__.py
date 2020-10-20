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
            logger.log(f"Error: {err.args[0]}")

        line = f"{argv[0]} ".join(line.split(f"{argv[0]} "))
        logger.debug(line)
