"""
foo bar baz
"""
from snadra.commands import CommandParser

def main():
    foo = CommandParser()
    foo.setup_prompt()
    foo.run()

if __name__ == "__main__":
    main()
