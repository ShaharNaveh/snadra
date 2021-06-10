import shlex
from typing import List, Optional, Tuple, Union

from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.patch_stdout import patch_stdout

from _snadra.cmd.commands import Commands


class CommandParser:
    """
    Responsible for handling the commands entered.

    Maps each command and it's arguments to the desired action.
    """

    def __init__(self) -> None:
        self.commands = Commands()

    async def dispatch_line(self, line: str) -> None:
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
            # NOTE: Here is where we initialize the command
            command = self.commands.get_command(argv[0])()  # type: ignore
        else:
            snutils.console.log(f"[red]Error[/red]: {repr(argv[0])} unknown command")
            return

        args: Union[str, List[str]] = argv[1:]
        args = [arg.encode("utf-8").decode("unicode_escape") for arg in args]

        try:
            if command.parser:
                args = command.parser.parse_args(args)
            else:
                args = pline
            await command.run(args)
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
        List[str]
            Line parsed as a list. (with shlex)
        str

        Raises
        ------
        ValueError
            If could not parse the line correctly.

        See Also
        --------
        shlex.split

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
