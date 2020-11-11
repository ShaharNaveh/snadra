import importlib
from importlib.machinery import SOURCE_SUFFIXES
import os
import pathlib
import sys
from typing import TYPE_CHECKING, Dict, Iterable, Optional, Sequence, Set, Tuple

import snadra._utils as snutils
from snadra._utils import SNADRA_DIR

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
        self, path: Optional["StrPath"] = None, *, skip: Optional[Sequence[str]] = None
    ) -> None:

        if path is None:
            self._path = pathlib.Path(__file__).parent.resolve()

        if skip:
            self._skip = skip
        else:
            self._skip = frozenset({"__init__"})

        fetched_modules = Commands._fetch_modules(
            file_paths=Commands.iter_dir(path=self._path, skip=self._skip)
        )
        self._commands_dict: Dict[str, "CommandDefinition"] = {
            keyword: module.Command
            for keyword, module in Commands._module_aliases(
                fetched_modules=fetched_modules
            )
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
        for path in file_paths:
            module_name = path.stem
            if module_name in sys.modules:
                # TODO: Do we ever reach here?
                snutils.console.log(f"Skiping already loaded module {module_name}")
                continue

            module_spec = importlib.util.spec_from_file_location(module_name, path)
            module = importlib.util.module_from_spec(module_spec)
            module_spec.loader.exec_module(module)
            yield module

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
