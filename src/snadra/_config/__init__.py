"""
Priority (high to low)
    - command line arguments
    - enviorment variables
    - config file
    - defaults # TODO
"""

import getopt
import os
from pathlib import Path
import sys
import typing

import toml

config: typing.Dict[str, typing.Optional[str]] = {
    "postgres_host": None,
    "postgres_user": None,
}


def setup_config():
    config_path = Path(os.environ["HOME"]) / ".config" / "snadra" / "config.toml"
    # cmd args

    # TODO:
    # maybe a list comprehension to get all keys from `config` and add '=' to the end
    options, _ = getopt.getopt(
        sys.argv[1:],
        "c:",
        [
            "config=",
            "postgres_host=",
            "postgres_user=",
        ],
    )

    for option, arg in options:
        if option in ("-c", "--config"):
            print(f"config path: {arg}")
            config_path = Path(arg)
            continue

        if option[2:] in config.keys():
            config[option[2:]] = arg

    # env vars + config file

    with config_path.open() as f:
        config_file_data = toml.loads(f.read())

    for config_name in config.keys():
        if config[config_name] is None:
            if (env_name := f"SNADRA_{config_name.upper()}") in os.environ:
                config[config_name] = os.environ[env_name]

            if config_name in config_file_data:
                config[config_name] = config_file_data[config_name]
