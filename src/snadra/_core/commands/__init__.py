import importlib
from importlib.machinery import SOURCE_SUFFIXES
import pathlib
import sys
from typing import TYPE_CHECKING, Dict, Iterable, Optional, Sequence, Set, Tuple

if TYPE_CHECKING:
    import os
    import types

    from snadra._core.base import CommandDefinition
    from snadra._typing import StrPath


class Commands:
    """
    foo bar baz.
    """
    # TODO: Add documentation.

    __slots__ = {"_commands_dict", "_path", "_skip"}

    def __init__(
        self, path: "StrPath" = ".", *, skip: Optional[Sequence[str]] = None
    ) -> None:
        self._path = pathlib.Path(path)

        if skip:
            self._skip = skip
        else:
            self._skip = frozenset({"__init__"})

        fetched_modules = Commands._fetch_modules(
                    file_paths=Commands.iter_dir(path=self._path, skip=self._skip)
                )
        self._commands_dict: Dict[str, "CommandDefinition"] = {
            keyword: module.Command
            for keyword, module in Commands._module_aliases(fetched_modules=fetched_modules)
        }

    @staticmethod
    def _fetch_modules(
        file_paths: Iterable["os.PathLike"],
    ) -> Iterable["types.ModuleType"]:
        """
        Get all modules from an iterable of file paths.

        Paramerters
        -----------
        file_paths : Iterable[:class:`os.PathLike`]
            Iterable of file paths of python modules, that will be loaded.

        Yields
        ------
        :class:`types.ModuleType`
            Module that contains a `Command` class.

        Notes
        -----
        Skipping already loaded modules.
        """
        for child in file_paths:
            module_name = child.stem

            if module_name in sys.modules:
                continue

            yield importlib.import_module(module_name)

    @staticmethod
    def _module_aliases(
        fetched_modules: Iterable["types.ModuleType"],
    ) -> Iterable[Tuple[str, "types.ModuleType"]]:
        """
        foo bar baz.
        """
        for module in fetched_modules:
            command = module.Command
            for keyword in command.KEYWORDS:
                yield keyword, module

    @staticmethod
    def iter_dir(
        path: "os.PathLike", *, skip: Sequence[str]
    ) -> Iterable["os.PathLike"]:
        """
        foo bar baz.
        """
        # TODO(maybe): Add recursive for dirs?
        for child in path.iterdir():
            if child.is_dir():
                continue
            if child.stem in skip:
                continue
            if child.suffix not in SOURCE_SUFFIXES:
                continue
            yield child

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


'''
class OldCommands:
    """
    Holds all the relevant commands attributes.

    Parameters
    ----------
    command_dirs : Union[str, List[str]]
        Sequence containing strings of paths to the command directories.
    ignore : Union[str, Iterable[str]], optional
        The module names to ignore.
    """

    # TODO: Change from "command_dirs" to "commands_dir"
    def __init__(
        self,
        *,
        command_dirs: "StrPath",
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
        command_dirs: str,
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
'''

if __name__ == "__main__":
    a = Commands()
