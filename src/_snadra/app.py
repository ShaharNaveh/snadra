from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.patch_stdout import patch_stdout

from _snadra.cmd.base import Commands
from _snadra.cmd.parsers import dispatch_line
from _snadra.cmd.utils import console
from _snadra.state import state


class SnadraApplication:
    def __init__(self):
        self.commands = Commands()
        self.config = ""
        self.current_workspace = ""

    async def run(self) -> None:  # pragma: no cover # TODO: Remove this pragma
        """
        The main loop.

        This is an infitine loop, until the user decides to exit.
        """
        self.__running = True

        while self.__running:
            try:
                current_workspace = state["current_workspace"]
                self.__prompt.message = f"({current_workspace}) snadra > "
                with patch_stdout():
                    line = await self.__prompt.prompt_async()
                await dispatch_line(line, commands=self.commands)
            except (EOFError, SystemExit):
                self.__running = False
            except KeyboardInterrupt:
                pass
            except Exception:
                # Unexpected errors, we catch them so the application won't crash.
                console.print_exception(width=None, show_locals=True)

    def _setup_prompt(self) -> None:  # pragma: no cover
        """
        See Notes section.

        Notes
        -----
        The only reason for this being in a seperate function is that it changes
        the `sys.stdout` and `sys.stderr` which disturbes `pytest`.
        """
        current_workspace = state["current_workspace"]
        self.__prompt: "PromptSession[str]" = PromptSession(
            f"({current_workspace}) snadra > ",
            auto_suggest=AutoSuggestFromHistory(),
            history=InMemoryHistory(),
            completer=WordCompleter(self.commands.keywords),
        )
