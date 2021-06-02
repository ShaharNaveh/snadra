"""
Main application entry point.

This gets ran when you execute:

$ snadra

or

$ python -m snadra
"""
import asyncio

from snadra._config import setupConfig
from snadra._core.parsers import CommandParser

if __name__ == "__main__":
    setupConfig()

    snadra_console = CommandParser()
    snadra_console._setup_prompt()
    asyncio.run(snadra_console.run())
