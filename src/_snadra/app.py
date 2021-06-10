import shlex
from typing import TYPE_CHECKING, List, Optional, Tuple, Union

from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.patch_stdout import patch_stdout

from _snadra.cmd import SnadraConsole
from _snadra.config import parse_config_file

if TYPE_CHECKING:
    import os


class SnadraApplication:
    __slots__ = {"config"}

    def __init__(self, config_file: "os.PathLike[str]"):
        self.config = parse_config_file(config_file)
