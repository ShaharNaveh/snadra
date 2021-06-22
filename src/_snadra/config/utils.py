import pathlib
from typing import Any, Dict

import rtoml


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
