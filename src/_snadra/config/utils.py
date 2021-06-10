from typing import TYPE_CHECKING

import rtoml

if TYPE_CHECKING:
    import pathlib


def parse_config_file(path: "pathlib.Path"):
    with path.open() as f:
        config_file_data = rtoml.loads(f.read())

    return config_file_data
