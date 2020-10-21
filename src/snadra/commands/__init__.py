"""
foo bar baz
"""
import os
import pkgutil
import shlex
from typing import TYPE_CHECKING, Iterable, List, Optional, Set, Union

from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import InMemoryHistory

import snadra
import snadra.utils as utils

if TYPE_CHECKING:
    from importlib.machinery import SourceFileLoader
    import types

    from snadra.commands._base import CommandDefinition

logger = utils.get_logger(__name__)


'''
def _get_commands_keywords(path: List[str]) -> Iterable[str]:
    """
    foo bar baz
    """
    snadra_dir = os.path.dirname(snadra.__file__)
    commands_dir = os.path.join(snadra_dir, "commands")
    path = [commands_dir]
    for module in _get_modules(path):
        command = module.Command()
        for keyword in command.KEYWORDS:
            yield keyword
'''


def _get_modules(path: List[str]) -> Iterable["types.ModuleType"]:
    """
    Gather the modules from a given path.

    Parameters
    ----------
    path : str
        Path where the modules are located.

    Yields
    ------
    types.ModuleType
        A module containing a `Command` class.
    """
    to_ignore = {"_base"}
    for loader, module_name, is_pkg in pkgutil.walk_packages(path):
        if module_name in to_ignore:
            continue
        yield loader.find_module(module_name).load_module(module_name)


def find_modules(
    path: List[str], *, to_ignore: Optional[Set[str]] = None
) -> Iterable["SourceFileLoader"]:
    """
    foo bar baz

    Parameters
    ----------
    path : List[str]
        Path where to find the modules.
    to_ignore : Set[str], default None
        Set of module names to ignore.

    Yields
    ------
    SourceFileLoader
    """
    if to_ignore is None:
        to_ignore = set()

    for loader, module_name, _ in pkgutil.walk_packages(path):
        if module_name in to_ignore:
            continue
        yield loader.find_module(module_name)

def load_module(module: "SourceFileLoader") -> "types.ModuleType":
    """
    Load a given module.

    Parameters
    ----------
    

    """
    return module.load_module(module.name)


class CommandParser:
    """
    Responsible for handling the commands entered.

    Maps each command and it's arguments to the desired action.
    """

    def __init__(self) -> None:
        self.commands: List["CommandDefinition"] = [
            command.Command() for command in _get_modules(__path__)  # type: ignore
        ]
        self.prompt: "PromptSession[str]" = PromptSession(
            "snadra > ",
            auto_suggest=AutoSuggestFromHistory(),
            history=InMemoryHistory(),
        )

    def run(self) -> None:
        """
        The main loop.

        This is an infitine loop, until the user decides to exit.
        """
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

    def dispatch_line(self, line: str) -> None:
        """
        Execute each command that was entered to the console.

        Parameters
        ----------
        line : str
            The full command (including arguments) as a string.
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
            if any(keyword == argv[0] for keyword in command.KEYWORDS):
                break
        else:
            logger.error(f"Error: {argv[0]}: unknown command")
            return

        args: Union[str, List[str]] = argv[1:]
        args = [arg.encode("utf-8").decode("unicode_escape") for arg in args]

        try:
            if command.parser:
                args = command.parser.parse_args(args)
            else:
                args = line
            command.run(args)
        except SystemExit:
            logger.debug("Incorrect arguments")
            return
