import abc
from typing import TYPE_CHECKING, Dict, FrozenSet

from rich.console import Console

if TYPE_CHECKING:
    from snadra._core.base import Parameter

console = Console()


class CommandABC(abc.ABC):
    """
    The generic structure for commands.

    Attributes
    ----------
    KEYWORDS : Set[str]
    DESCRIPTION : str
        Help text for the new command.
    LONG_HELP : str
        Long help for the command.
    ARGS : Dict[str, snadra._core.base.Parameter]
        Dictionary of parameter definitions created with the :class:`Parameter` class.
        If this is None, your command will receive the
        raw argument string and no processing will be done except
        removing the leading command name.
    GROUPS : Dict[str, snadra._core.base.Group]
        Dictionary mapping group definitions to group names.
        The parameters to Group are passed directly to either
        add_argument_group or add_mutually_exclusive_group with the exception of the
        mutex arg, which determines the group type.
    """

    @property
    @classmethod
    @abc.abstractmethod
    def keywords(cls) -> FrozenSet[str]:
        """
        Keywords for the new command.

        Can be treated as command "aliases".

        Returns
        -------
        frozenset of str
            Keywords for the command.
        """
        return NotImplementedError

    @property
    @classmethod
    @abc.abstractmethod
    def description(cls) -> str:
        """
        Command description.

        Returns
        -------
        str
            The description for the command.
        """
        return NotImplementedError

    @property
    @classmethod
    @abc.abstractmethod
    def long_help(cls) -> str:
        """
        Long help text for the new command.

        Returns
        -------
        str
            Long help text for the command.
        """
        return NotImplementedError

    @property
    @classmethod
    @abc.abstractmethod
    def arguments(cls) -> Dict[str, "Parameter"]:
        """
        Arguments for the new command.
        Dictionary of parameter definitions created with the :class:`Parameter` class.
        If this is None, your command will receive the
        raw argument string and no processing will be done except
        removing the leading command name.
        """
        return NotImplementedError
