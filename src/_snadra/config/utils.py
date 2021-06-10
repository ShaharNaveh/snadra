import pathlib
from typing import TYPE_CHECKING

import rtoml

if TYPE_CHECKING:
    import os


def parse_config_file(path: "os.PathLike[str]"):
    with path.open() as file_obj:
        config_file_data = rtoml.load(file_obj)

    return config_file_data


def config_file_location() -> pathlib.Path:
    """
    Gets the location of the configuration file.

    The search hierarchy is:
        * $HOME/.config/snadra/snadra_config.toml
        * $HOME/.snadra_config.toml
        * ./default_config.toml
    """
    _locations = [
        "~/.config/snadra/snadra_config.toml",
        "~/.snadra_config.toml",
        "./default_config.toml",
    ]

    locations = [pathlib.Path(location).expanduser() for location in _locations]

    for location in locations:
        print(location)
        if location.exists():
            return location
