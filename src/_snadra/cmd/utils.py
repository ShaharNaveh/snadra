import abc
import argparse
import sys as _sys
from typing import Any, Dict, Optional, Set

from rich.console import Console

console = Console(emoji=False)


class SnadraArgumentParser(argparse.ArgumentParser):
    """
    This class is just for fixing the
     `exit` method, so it won't use sys.exit.

    https://github.com/python/cpython/blob/bc6c12c72a9536acc96e7b9355fd69d1083a43c1/Lib/argparse.py#L2559

    """

    def exit(self, status=0, message=None):
        if message:
            self._print_message(message, _sys.stderr)


class CommandMeta(metaclass=abc.ABCMeta):
    """
    Abstract base class for command line commands.
    """

    def __init__(self) -> None:
        self.parser = SnadraArgumentParser(
            prog=self.keyword,
            description=self.description,
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
        if self.arguments is not None:
            self.build_parser(self.parser, self.arguments)

    def build_parser(
        self,
        parser: argparse.ArgumentParser,
        args: Dict[str, Dict[str, Any]],
    ) -> None:
        """
        Parse the ARGS and DEFAULTS dictionaries to build an argparse ArgumentParser
        for this command. You should not need to overload this.

        Parameters
        ----------
        parser : argparse.ArgumentParser
            Parser object to add arguments to.
        args : Dict[str, Dict]
            `ARGS` dictionary.
        """
        for arg, param in args.items():
            names = arg.split(",")
            group = parser

            group.add_argument(*names, **param)

        if self.defaults is not None:
            parser.set_defaults(**self.defaults)

    @property
    def defaults(self) -> Dict:
        """
        Set default value for the specific argument.

        This is the same as:
        parser.set_defaults(foo='spam')

        Returns
        -------
        Dict
        """
        ...

    @property
    @abc.abstractmethod
    def keyword(self) -> str:
        """
        Keyword for the new command.

        Returns
        -------
        str
            Keyword for the command.
        """
        ...

    @property
    @abc.abstractmethod
    def aliases(self) -> Optional[Set[str]]:
        """
        Aliases for the command.

        The main difference between "keyword" and "aliases", is that the aliases
        do not apear (by default) in the help menu.

        Returns
        -------
        set of str, or None
            Aliases for the command.
        """
        ...

    @property
    @abc.abstractmethod
    def description(self) -> str:
        """
        Command description.

        Returns
        -------
        str
            The description for the command.
        """
        ...

    @property
    @abc.abstractmethod
    def long_help(self) -> str:
        """
        Long help text for the new command.

        This gets displayed when:

        $ help <command>

        is ran.

        Returns
        -------
        str
            Long help text for the command.
        """
        ...

    @property
    def arguments(self) -> Optional[Dict[str, Dict[str, Any]]]:
        """
        Arguments for the new command.

        Parameters to pass into :meth:`argparse.ArgumentParser.add_argument`
        If this is None, your command will receive the
        raw argument string and no processing will be done except
        removing the leading command name.
        """
        ...

    @abc.abstractmethod
    async def run(self, args: argparse.Namespace) -> None:
        """
        Implementation for the new command.

        This is responsible for the actual action of the command.
        """
        ...
