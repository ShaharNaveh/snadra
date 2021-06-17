import abc
import argparse
from typing import TYPE_CHECKING, Dict, Optional, Set

from rich.console import Console

if TYPE_CHECKING:
    from _snadra.cmd.base import Parameter


console = Console()


class CommandMeta(metaclass=abc.ABCMeta):
    """
    Abstract base class for command line commands.
    """

    def __init__(self) -> None:
        if self.arguments is not None:
            self.parser = argparse.ArgumentParser(
                prog=self.keyword,
                description=self.description,
                formatter_class=argparse.RawDescriptionHelpFormatter,
            )
            self.build_parser(self.parser, self.arguments)
        else:
            self.parser = None  # type: ignore

    def build_parser(
        self,
        parser: argparse.ArgumentParser,
        args: Dict[str, "Parameter"],
    ) -> None:
        """
        Parse the ARGS and DEFAULTS dictionaries to build an argparse ArgumentParser
        for this command. You should not need to overload this.

        Parameters
        ----------
        parser : argparse.ArgumentParser
            Parser object to add arguments to.
        args : Dict[str, _snadra.cmd.base.Parameter]
            `ARGS` dictionary.
        """
        for arg, param in args.items():
            names = arg.split(",")
            group = parser

            group.add_argument(*names, *param.args, **param.kwargs)

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

        Returns
        -------
        str
            Long help text for the command.
        """
        ...

    @property
    @abc.abstractmethod
    def arguments(self) -> Dict[str, "Parameter"]:
        """
        Arguments for the new command.

        Dictionary of parameter definitions created with the `Parameter` class.
        If this is None, your command will receive the
        raw argument string and no processing will be done except
        removing the leading command name.

        See Also
        --------
        snadra._core.base.Parameter
        """
        ...

    @abc.abstractmethod
    async def run(self, args: argparse.Namespace) -> None:
        """
        Implementation for the new command.

        This is responsible for the actual action of the command.
        """
        ...
