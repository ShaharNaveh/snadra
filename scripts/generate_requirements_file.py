#!/usr/bin/env python3
# TODO:
# Add tests for this script.

# TODO:
# Integrate this script with the CI

import argparse
import configparser
import os
import pathlib
import sys
from typing import Union

BASE_DIR = pathlib.Path(__file__).parents[1]
__SCRIPT_PATH = pathlib.Path(__file__).relative_to(BASE_DIR)
WARNING = (
    f"# This file is auto-generated from {__SCRIPT_PATH}, do not edit directly.\n"
    "# If you wish to edit the dependencies,"
    " edit the 'install_requires' in 'setup.cfg'.\n\n"
)


def get_config(config_file: Union[pathlib.Path, str]) -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read(str(config_file))
    return config


def requirements_content(
    configuration: configparser.ConfigParser, header=WARNING
) -> str:
    dependencies = (configuration["options"]["install_requires"]).strip()
    file_content = f"{header}\n{dependencies}"

    return file_content


def main(args):
    config_file = (BASE_DIR / "setup.cfg").resolve()
    configuration = get_config(config_file=config_file)

    req_file = (BASE_DIR / "requirements.txt").resolve()

    data = requirements_content(configuration=configuration, header=WARNING)

    if args.check:
        if not req_file.is_file():
            sys.exit(1)

        with req_file.open(mode="r") as file_obj:
            current_data = file_obj.read()

        if current_data == data:
            print("'requirements.txt' file is up to date")
            sys.exit(0)
        else:
            prefix = ""
            if os.environ["GITHUB_ACTIONS"] == "true":
                prefix = "##[error] "
            print(f"{prefix}'requirements.txt' file is not up to data", file=sys.stderr)
            sys.exit(1)

    with req_file.open(mode="w") as file_obj:
        file_obj.write(data)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Generate 'requirements.txt' file")
    argparser.add_argument(
        "-c",
        "--check",
        default=False,
        action="store_true",
        help="Check if the current 'requirements.txt' file is updated",
    )

    args = argparser.parse_args()
    main(args)
