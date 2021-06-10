from typing import TYPE_CHECKING

import rtoml

if TYPE_CHECKING:
    import pathlib


def parse_config_file(path: "pathlib.Path"):
    with path.open() as file_obj:
        config_file_data = rtoml.load(file_obj)

    return config_file_data
