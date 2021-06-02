"""
Priority (high to low)
    - command line arguments
    - enviorment variables
    - config file # TODO
    - defaults # TODO
"""

import getopt
import os
import sys
import typing

config: typing.Dict[str, typing.Optional[str]] = {
    "postgres_host": None,
    "postgres_user": None,
}


def setupConfig():
    # cmd args

    # TODO:
    # maybe a list comprehension to get all keys from `config` and add '=' to the end
    options, _ = getopt.getopt(sys.argv[1:], "", ["postgres_host=", "postgres_user="])

    for option, arg in options:
        if option[2:] in config.keys():
            config[option[2:]] = arg

    # env vars

    for config_name in config.keys():
        if config[config_name] is None:
            if (env_name := f"SNADRA_{config_name.upper()}") in os.environ:
                config[config_name] = os.environ[env_name]
