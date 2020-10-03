#!/usr/bin/env python3
import re

from setuptools import setup

with open("src/snadra/__init__.py", mode="r", encoding="utf8") as init_file:
    version = re.search(r'__version__ = "(.*?)"', init_file.read()).group(1)

if __name__ == "__main__":
    setup(name="snadra", version=version, install_requires=[], extras_require={})
