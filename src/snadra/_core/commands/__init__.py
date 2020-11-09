import pkgutil
from typing import TYPE_CHECKING, Dict, Iterable, List, Optional, Set, Union

from snadra._core.base import CommandDefinition

if TYPE_CHECKING:
    from importlib.machinery import SourceFileLoader


class Commands:
    """
    Holds all the relevant commands attributes.

    Parameters
    ----------
    command_dirs : Union[str, List[str]]
        Sequence containing strings of paths to the command directories.
    ignore : Union[str, Iterable[str]], optional
        The module names to ignore.
    """

    def __init__(
        self,
        *,
        command_dirs: Union[str, List[str]],
        ignore: Optional[Union[str, Iterable[str]]] = None,
    ) -> None:
        if isinstance(command_dirs, str):
            command_dirs = [command_dirs]

        self._commands_dict = self._refresh_command_dict(
            command_dirs=command_dirs, ignore=ignore
        )

    def _refresh_command_dict(
        self,
        *,
        command_dirs: List[str],
        ignore: Optional[Union[str, Iterable[str]]] = None,
    ) -> Dict[str, "CommandDefinition"]:
        """
        Map every keyword to the desired command.

        Parameters
        ----------
        command_dirs : List[str]
            List containing string representation of paths to the command directories.
        ignore : Union[str, Iterable[str]], optional
            The module names to ignore.

        Returns
        -------
        Dict[str, :class:`CommandDefinition`]
            Dictionary with the keywords mapped to thier command.
        """
        commands_dict = {}
        for module in Commands._find_modules(path_list=command_dirs, ignore=ignore):
            # TODO: Should we remove the () from the Command,
            # should not run this until we have too?
            command = module.load_module(module.name).Command()  # type: ignore
            for keyword in command.KEYWORDS:
                commands_dict[keyword] = command
        return commands_dict

    def get_command(self, keyword: str) -> Optional["CommandDefinition"]:
        """
        Get the command that mapped to a keyword.

        Parameters
        ----------
        keyword : str
            Keyword to check.

        Returns
        -------
        Optional[:class:`CommandDefinition`]
            The command that is mapped to ``keyword``,
            if ``keyword`` is not mapped to any command, `None` is returned.
        """
        return self._commands_dict.get(keyword)

    def is_valid_keyword(self, keyword: str) -> bool:
        """
        Check if a given keyword is mapped to a valid command.

        Parameters
        ----------
        keyword : str
            Keyword to check.

        Returns
        -------
        bool
            Whether or not the keyword is mapped to a valid command.
        """
        return keyword in self._commands_dict

    @property
    def keywords(self) -> Set[str]:
        """
        Get all the available keywords.

        Returns
        -------
        Set[str]
            All the available keywords.
        """
        return set(self._commands_dict.keys())

    @staticmethod
    def _find_modules(
        path_list: List[str], *, ignore: Optional[Union[str, Iterable[str]]] = None
    ) -> Iterable["SourceFileLoader"]:
        """
        Find modules in a given path.

        Parameters
        ----------
        path : List[str]
            Path where to find the modules.
        ignore : Union[str, Iterable[str]], optional
            Set of module names to skip.

        Yields
        ------
        :class:`SourceFileLoader`
        """
        if ignore is None:
            ignore = set()

        for loader, module_name, _ in pkgutil.walk_packages(path_list):
            if module_name in ignore:
                continue
            yield loader.find_module(module_name)
