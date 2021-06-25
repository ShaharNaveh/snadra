import shlex
from typing import TYPE_CHECKING, List, Optional

from _snadra.cmd.utils import console

if TYPE_CHECKING:
    from _snadra.cmd.base import Commands


async def dispatch_line(line: str, *, commands: "Commands") -> None:
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
        # TODO:
        # Add memozation
        command = commands.get_command(target_command)()  # type: ignore
        parser = command.parser
    else:
        console.log(f"[red]Error[/red]: {repr(target_command)} unknown command")
        return

    command_arguments = pline[1:]

    # TODO:
    # Maybe warn the user if got unknown args?
    known_args, _ = parser.parse_known_args(command_arguments)

    await command.run(known_args)


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

    try:
        parsed_line = shlex.split(line)
    except ValueError as err:
        console.log(f"[red]Error[/red]: {err.args[0]}")
        return None

    return parsed_line
