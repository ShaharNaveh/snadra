import shlex
from typing import List, Optional, Tuple, Union

from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.patch_stdout import patch_stdout

from _snadra.cmd.commands import Commands
from _snadra.cmd.utils import console


async def dispatch_line(line: str, *, commands: Commands) -> None:
    """
    Execute each command that was entered to the console.

    Parameters
    ----------
    line : str
        The full command (including arguments) as a string.
    commands : Commands
        Commands object.
    """
    pline = parse_line(line=line)
    if pline is None:
        return

    target_command = pline[0]

    if commands.is_valid_keyword(target_command):
        command = commands.get_command(target_command)()  # type: ignore
        parser = command.parser
    else:
        console.log(f"[red]Error[/red]: {repr(target_command)} unknown command")
        return

    command_arguments = pline[1:]
    args_namespace = parser.parse_args(command_arguments)

    await command.run(args_namespace)


def parse_line(line: str) -> Optional[List[str]]:
    """
    Parameters
    ----------
    line : str
        The full command (including arguments).

    Returns
    -------
    List[str]
        Line parsed (with shlex) as a list.

    See Also
    --------
    shlex.split

    Examples
    --------
    >>> line = "command --target 127.0.0.1 --port 80"
    >>> parse_line(line)
    ['command', '--target', '127.0.0.1', '--port', '80']
    """
    line = line.strip()
    if line == "":
        return None

    parsed_line = shlex.split(line)
    return parsed_line


class CommandParser:
    """
    Responsible for handling the commands entered.

    Maps each command and it's arguments to the desired action.
    """

    def __init__(self) -> None:
        self.commands = Commands()

    def _setup_prompt(self) -> None:  # pragma: no cover
        """
        See Notes section.

        Notes
        -----
        The only reason for this being in a seperate function is that it changes
        the `sys.stdout` and `sys.stderr` which disturbes `pytest`.
        """
        self.__prompt: "PromptSession[str]" = PromptSession(
            "snadra > ",
            auto_suggest=AutoSuggestFromHistory(),
            history=InMemoryHistory(),
            completer=WordCompleter(self.commands.keywords),
        )

    async def run(self) -> None:  # pragma: no cover # TODO: Remove this pragma
        """
        The main loop.

        This is an infitine loop, until the user decides to exit.
        """
        self.__running = True

        while self.__running:
            try:
                with patch_stdout():
                    line = await self.__prompt.prompt_async()
                line = line.strip()
                if line == "":
                    continue
                await dispatch_line(line, commands=self.commands)
            except EOFError:
                self.__running = False
                continue
            except KeyboardInterrupt:
                continue
            except Exception:
                # Unexpected errors, we catch them so the application won't crash.
                console.print_exception(width=None, show_locals=True)
