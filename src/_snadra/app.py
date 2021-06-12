from typing import TYPE_CHECKING

from _snadra.config import parse_config_file

if TYPE_CHECKING:
    import os


class SnadraApplication:
    __slots__ = {"config"}

    def __init__(self, config_file: "os.PathLike[str]"):
        self.config = parse_config_file(config_file)
