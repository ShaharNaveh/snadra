"""
Main application entry point.

This gets ran when you execute:

$ snadra

or

$ python -m snadra
"""
from snadra._core.parsers import CommandParser

if __name__ == "__main__":
    snadra_console = CommandParser()
    snadra_console.setup_prompt()
    snadra_console.run()
