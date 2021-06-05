import pathlib
import typing

import rtoml


def parse_config_file(path: pathlib.Path) -> typing.Dict[str, typing.Any]:
    with path.open() as f:
        config_file_data = rtoml.loads(f.read())

    return config_file_data
