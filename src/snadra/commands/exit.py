"""
foo
"""
from snadra.commands._base import CommandDefinition


class Command(CommandDefinition):
    """
    Help message for "exit"
    """

    PROG = "exit"

    def run(self, args):
        raise EOFError
