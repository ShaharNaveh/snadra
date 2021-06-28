import pathlib
from typing import Any, Dict

import rtoml

from _snadra.cmd.utils import console
from _snadra.config.constants import DEFAULT_CONFIG


def parse_config_file(path: pathlib.Path) -> Dict[str, Any]:
    """
    Parse the configuration file.

    Parameters
    ----------
    path : pathlib.Path
        Path to the configuration file.

    Returns
    -------
    Dict[str, Any]
        Dictionary of the configuration file.
    """
    with path.open() as file_obj:
        config = rtoml.load(file_obj)

    return config


def get_config(path: pathlib.Path) -> Dict[str, Any]:
    """
    Get the configuration object.

    Parameters
    ----------
    path : pathlib.Path
        Path to the configuration file.

    Returns
    -------
    Dict[str, Any]
        Dictionary of the configuration file.
    """
    if path.exists():
        config = parse_config_file(path=path)
        return config

    console.log("Config file missing; Using default config")
    return DEFAULT_CONFIG
