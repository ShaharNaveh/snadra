import shlex
from typing import List, Optional, Tuple, Union

from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import InMemoryHistory

from snadra._core.base import Commands
import snadra._utils as snutils


class CommandParser:
    """
    Responsible for handling the commands entered.

    Maps each command and it's arguments to the desired action.
    """

    def __init__(self) -> None:
        core_commands_dir = snutils.get_core_commands_dir()
        self.commands = Commands(command_dirs=core_commands_dir)

    def setup_prompt(self) -> None:  # pragma: no cover
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
                snutils.console.print_exception(width=None)
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
            snutils.console.log(f"[red]Error[/red]: {repr(argv[0])} unknown command")
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
            snutils.console.log("Incorrect arguments")
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

        Examples
        --------
        >>> line = "command --target 127.0.0.1 --port 80"
        >>> CommandParser._parse_line(line)
        (\
['command', '--target', '127.0.0.1', '--port', '80'], \
'command --target 127.0.0.1 --port 80')
        """
        line = line.strip()
        if line == "":
            return None

        try:
            argv = shlex.split(line)
        except ValueError as err:
            snutils.console.log(f"[red]Error[/red]: {err.args[0]}")
            return None

        pline = f"{argv[0]} ".join(line.split(f"{argv[0]} "))
        return (argv, pline)
