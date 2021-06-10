import shlex
from typing import TYPE_CHECKING, List, Optional, Tuple, Union

from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.patch_stdout import patch_stdout

from _snadra.cmd import CommandParser, SnadraConsole
from _snadra.config import parse_config_file

if TYPE_CHECKING:
    import os


class SnadraApplication:
    def __init__(self, config_file: "os.PathLike[str]"):
        self._console = SnadraConsole()
        self.__parser = CommandParser()
        # TODO:
        # Uncomment this
        # self.config = parse_config_file(config_file)

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
                await self.__parser.dispatch_line(line)
            except EOFError:
                self.__running = False
                continue
            except KeyboardInterrupt:
                continue
            except Exception:
                # Unexpected errors, we catch them so the application won't crash.
                self._console.print_exception(width=None, show_locals=True)
