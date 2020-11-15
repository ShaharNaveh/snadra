import abc
from typing import TYPE_CHECKING, Dict, Set

from rich.console import Console

if TYPE_CHECKING:
    import argparse

    from snadra._core.base import Parameter

console = Console()


class CommandMeta(metaclass=abc.ABCMeta):
    """
    Abstract base class for command line commands.

    See Also
    --------
    snadra._core.commands.exit
    snadra._core.commands.help
    """

    @property
    @abc.abstractmethod
    def keywords(self) -> Set[str]:
        """
        Keywords for the new command.

        Can be treated as command "aliases".

        Returns
        -------
        set of str
            Keywords for the command.
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
    def run(self, args: "argparse.Namespace") -> None:
        """
        Implementation for the new command.

        This is responsible for the actual action of the command.
        """
        ...
