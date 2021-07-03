import pathlib
import pkgutil
import sys
from typing import TYPE_CHECKING, Iterable, Optional, Set

if TYPE_CHECKING:
    import types

    from _snadra.cmd.utils import CommandMeta


class Commands:
    """
    Holds all the relevant commands attributes.

    Parameters
    ----------
    path : pathlib.Path, optional.
        Path to the directory with the commands to load.
        If not specified, the snadra's core commands directory is being loaded.
        Sequence containing strings of paths to the command directories.
    skip : Union[Sequence[str], Set[str], FrozenSet[str]]], optional.
        Module names to skip.

    Notes
    -----
    The module names inside `skip`, should not be with a file suffix.
    """

    __slots__ = {"_commands_alias", "_commands_core", "commands"}

    def __init__(
        self,
        path: Optional[pathlib.Path] = None,
        skip: Optional[Set[str]] = None,
    ) -> None:
        if path is None:
            path = pathlib.Path(__file__).parent / "commands"

        modules = Commands.fetch_modules(path, skip=skip)

        self._commands_core = {}
        self._commands_alias = {}

        for module in modules:
            command = module.Command  # type: ignore
            core_keyword = command.keyword
            self._commands_core[core_keyword] = command
            if command.aliases is None:
                continue

            for alias in command.aliases:
                self._commands_alias[alias] = command

        self.commands = {**self._commands_alias, **self._commands_core}

    @staticmethod
    def fetch_modules(
        *paths: Iterable[pathlib.Path],
        _prefix: str = None,
        skip: Optional[Set[str]] = None,
    ) -> Iterable["types.ModuleType"]:
        """
        Get all modules from an iterable of file paths.

        Parameters
        ----------
        paths : Iterable[pathlib.Path]
            Iterable of file paths of python modules, that will be loaded.
        _prefix : str
        skip : Set[str]
            Modules names to skip.

        Yields
        ------
        types.ModuleType
            Module that contains a `Command` class.

        Notes
        -----
        Skipping already loaded modules.
        """
        if _prefix is None:
            _prefix = "_snadra.cmd.commands."

        if skip is None:
            skip = set()

        path_lst = [str(path) for path in paths]
        for loader, module_name, _ in pkgutil.walk_packages(path_lst, prefix=_prefix):
            name = module_name.split(_prefix)[1]

            if name in skip:
                continue

            if module_name not in sys.modules:
                module = loader.find_module(module_name).load_module(module_name)
            else:
                module = sys.modules[module_name]

            yield module

    @property
    def aliases(self) -> Set[str]:
        """
        Get all keywords that are aliases.

        Returns
        -------
        Set[str]
            All aliases keywords.
        """
        return set(self._commands_alias.keys())

    @property
    def keywords(self) -> Set[str]:
        """
        Get all core keywords.

        Returns
        -------
        Set[str]
            All core keywords.
        """
        return set(self._commands_core.keys())

    @property
    def all_keywords(self) -> Set[str]:
        """
        Get both the core keywords and the aliases keywords.

        Returns
        -------
        Set[str]
            All the available keywords.
        """
        return set(self.commands.keys())

    def get_command(self, keyword: str) -> Optional["CommandMeta"]:
        """
        Get the command that is mapped to a keyword.

        Parameters
        ----------
        keyword : str
            Keyword to check.

        Returns
        -------
        Optional[:class:`CommandMeta`]
            The command that is mapped to ``keyword``,
            if ``keyword`` is not mapped to any command, `None` is returned.
        """
        return self.commands.get(keyword)

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
        return keyword in self.commands
