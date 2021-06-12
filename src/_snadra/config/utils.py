import pathlib
from typing import TYPE_CHECKING

import rtoml

if TYPE_CHECKING:
    import os


def parse_config_file(path: "os.PathLike[str]"):
    with path.open() as file_obj:  # type: ignore
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
    locations = [
        pathlib.Path("~/.config/snadra/snadra_config.toml").expanduser(),
        pathlib.Path("~/.snadra_config.toml").expanduser(),
    ]

    for location in locations:
        print(location)
        if location.exists():
            return location

    default_config_file_location = (
        pathlib.Path(__file__).parent / "default_config.toml"
    ).resolve()

    return default_config_file_location
