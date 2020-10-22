"""
foo bar baz
"""
from snadra.commands import CommandParser


def main():
    snadra_console = CommandParser()
    snadra_console.setup_prompt()
    snadra_console.run()


if __name__ == "__main__":
    main()
