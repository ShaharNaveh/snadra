"""
foo bar baz
"""
import pkgutil
import shlex
from typing import TYPE_CHECKING, Dict, Iterable, List, Optional, Set, Tuple, Union

from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import InMemoryHistory

import snadra.utils as utils

if TYPE_CHECKING:
    from importlib.machinery import SourceFileLoader
    import types

    from snadra.commands._base import CommandDefinition

logger = utils.get_logger(__name__)


class Commands:
    # TODO: Is it good that a lot of stuff here are properties?

    def __init__(self) -> None:
        # TODO: This feels wrong, but it works *facepalm*
        self.command_map: Dict[str, "CommandDefinition"] = self._refresh()

    @property
    def keywords(self) -> Set[str]:
        """
        Get all the available keywords.

        Returns
        -------
        Set[str]
            All the available keywords.
        """
        result: Set[str] = set()
        for command in self.available_commands:
            for keyword in command.KEYWORDS:
                result.add(keyword)
        return result

    def is_valid_keyword(self, keyword: str) -> bool:
        """
        Check if a given keyword is mapped to a valid command.

        Parameters
        ----------
        keyword : str
            Keyword to check.

        Returns
        -------
        bool
            Whether or not the keyword is mapped to a valid command.
        """
        return keyword in self.keywords

    def get_command(self, keyword: str) -> Optional["CommandDefinition"]:
        """
        Get the command that mapped to a keyword.

        Parameters
        ----------
        keyword : str
            Keyword to check.

        Returns
        -------
        CommandDefinition, or None
            The command that is mapped to `keyword`, if `keyword` is not mapped to any
            command, `None` is returned.
        """
        for command in self.available_commands:
            if keyword in command.KEYWORDS:
                return command
        return None

    @property
    def available_commands(self) -> Set["CommandDefinition"]:
        """
        Get all the available keywords.

        Returns
        -------
        Set[CommandDefinition]
            All the available commands.
        """
        return {module.load_module(module.name).Command() for module in self._modules}

    @property
    def _modules(self) -> Set["SourceFileLoader"]:
        return {
            module for module in Commands.find_modules(__path__, to_ignore={"_base"})  # type: ignore # noqa: E501
        }

    def _refresh(self) -> Dict[str, "CommandDefinition"]:
        return {keyword: self.get_command(keyword) for keyword in self.keywords}

    @staticmethod
    def find_modules(
        path: List[str], *, to_ignore: Optional[Set[str]] = None
    ) -> Iterable["SourceFileLoader"]:
        """
        Find modules in a given path.

        Parameters
        ----------
        path : List[str]
            Path where to find the modules.
        to_ignore : Set[str], optional
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


class CommandParser:
    """
    Responsible for handling the commands entered.

    Maps each command and it's arguments to the desired action.
    """

    def __init__(self) -> None:
        self.commands = Commands()

    def setup_prompt(self):  # pragma: no cover
        """
        See Notes section.

        Notes
        -----
        The only reason for this being in a seperate function is that it changes
        the `sys.stdout` and `sys.stderr` which disturbes `pytest`.
        """
        self.prompt: "PromptSession[str]" = PromptSession(
            "snadra > ",
            auto_suggest=AutoSuggestFromHistory(),
            history=InMemoryHistory(),
        )

    def run(self) -> None:  # pragma: no cover # TODO: Remove this pragma
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
            except Exception as err:
                logger.debug("We got an exception which we do not handle")
                logger.debug(f"{repr(type(err).__name__)}: {err}")
                continue

    @staticmethod
    def _parse_line(line: str) -> Optional[Tuple[List[str], str]]:
        """
        Parameters
        ----------
        line : str
            The full command (including arguments).

        Returns
        -------
        Optional[Tuple[List[str], str]]
            Tuple with the line as a list.
            and the parsed line.

        Raises
        ------
        ValueError
            If could not parse the line correctly.
        """
        line = line.strip()
        if line == "":
            return None

        try:
            argv = shlex.split(line)
        except ValueError as err:
            logger.error(f"Error: {err.args[0]}")
            return None

        pline = f"{argv[0]} ".join(line.split(f"{argv[0]} "))
        return (argv, pline)

    '''
    def has_command(self, keyword: str) -> bool:
        """
        Check if a given keyword is mapped to a valid command.

        Parameters
        ----------
        keyword : str
            Keyword to check.

        Returns
        -------
        bool
            Whether or not the keyword is mapped to a valid command.
        """
        return keyword in self.keywords
    '''

    '''
    def get_command(self, keyword: str):
        """
        Get the command that mapped to a keyword.

        Parameters
        ----------
        keyword : str
            Keyword to check.
        """
        for command in self.commands:
            if keyword in command.KEYWORDS:
                return command
        return None
    '''

    def dispatch_line(self, line: str) -> None:
        """
        Execute each command that was entered to the console.

        Parameters
        ----------
        line : str
            The full command (including arguments) as a string.
        """
        try:
            argv, pline = CommandParser._parse_line(line=line)  # type: ignore
        except TypeError:
            return

        if self.commands.is_valid_keyword(argv[0]):
            command = self.commands.get_command(argv[0])
        else:
            logger.error(f"Error: {argv[0]}: unknown command")
            return

        args: Union[str, List[str]] = argv[1:]
        args = [arg.encode("utf-8").decode("unicode_escape") for arg in args]

        try:
            if command.parser:
                args = command.parser.parse_args(args)
            else:
                args = pline
            command.run(args)
        except SystemExit:
            logger.debug("Incorrect arguments")
            return
