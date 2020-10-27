"""
foo bar baz
"""
import logging
import pkgutil
import shlex
from typing import TYPE_CHECKING, Dict, Iterable, List, Optional, Set, Tuple, Union

from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import InMemoryHistory

from snadra._util import console

if TYPE_CHECKING:
    from importlib.machinery import SourceFileLoader

    from snadra.commands._base import CommandDefinition

logger = logging.getLogger(__name__)


class Commands:
    """
    Holds all the relevant commands attributes.
    """

    def __init__(self) -> None:
        self._commands_dict = self._refresh_command_dict()

    def _refresh_command_dict(self) -> Dict[str, "CommandDefinition"]:
        """
        foo bar baz
        """
        commands_dict: Dict[str, "CommandDefinition"] = {}

        for module in Commands.find_modules(__path__, to_ignore={"_base"}):  # type: ignore # noqa: E501
            command = module.load_module(module.name).Command()  # type: ignore
            for keyword in command.KEYWORDS:
                commands_dict[keyword] = command
        return commands_dict

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
        return self._commands_dict.get(keyword)

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
        return keyword in self._commands_dict

    @property
    def available_commands(self) -> Set["CommandDefinition"]:
        """
        Get all the available keywords.

        Returns
        -------
        Set[CommandDefinition]
            All the available commands.
        """
        return set(self._commands_dict.values())

    @property
    def keywords(self) -> Set[str]:
        """
        Get all the available keywords.

        Returns
        -------
        Set[str]
            All the available keywords.
        """
        return set(self._commands_dict.keys())

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
            except Exception:
                # Unexpected errors, we catch them so the application won't crash.
                console.print_exception(width=None)
                continue

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
            console.log(f"[red]Error[/red]: {repr(argv[0])} unknown command")
            return

        args: Union[str, List[str]] = argv[1:]
        args = [arg.encode("utf-8").decode("unicode_escape") for arg in args]

        try:
            if command.parser:  # type: ignore
                args = command.parser.parse_args(args)  # type: ignore
            else:
                args = pline
            command.run(args)  # type: ignore
        except SystemExit:
            console.log("Incorrect arguments")
            return

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
            console.log(f"[red]Error[/red]: {err.args[0]}")
            return None

        pline = f"{argv[0]} ".join(line.split(f"{argv[0]} "))
        return (argv, pline)
