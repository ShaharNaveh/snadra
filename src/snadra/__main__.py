"""
foo bar baz
"""
from snadra.commands import CommandParser


if __name__ == "__main__":
    snadra_console = CommandParser()
    snadra_console.setup_prompt()
    snadra_console.run()
