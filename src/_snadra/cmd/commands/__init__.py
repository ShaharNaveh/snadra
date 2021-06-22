import importlib
from importlib.machinery import SOURCE_SUFFIXES
import importlib.util
import pathlib
import sys
from typing import TYPE_CHECKING, FrozenSet, Iterable, Optional, Sequence, Set, Union

if TYPE_CHECKING:
    import argparse
    import os
    import types

    from _snadra.cmd.utils import CommandMeta


class Commands:
    """
    Holds all the relevant commands attributes.

    Parameters
    ----------
    path : os.PathLike[str], optional.
        Path to the directory with the commands to load.
        If not specified, the snadra's core commands directory is being loaded.
        Sequence containing strings of paths to the command directories.
    skip : Union[Sequence[str], Set[str], FrozenSet[str]]], optional.
        Module names to skip.

    Notes
    -----
    The module names inside `skip`, should not be with a file suffix.
    """

    __slots__ = {
        "_commands_alias",
        "_commands_core",
        "_path",
        "_skip",
        "commands",
    }

    def __init__(
        self,
        path: Optional["os.PathLike[str]"] = None,
        *,
        skip: Optional[Set[str]] = None,
    ) -> None:
        this_file = pathlib.Path(__file__)
        if path is None:
            self._path = this_file.parent.resolve()
        else:
            self._path = pathlib.Path(path)

        self._skip: Set[str] = {this_file.stem}

        if skip is not None:
            self._skip = self._skip.union(skip)

        modules = Commands._fetch_modules(
            file_paths=Commands.iter_dir(path=self._path, skip=self._skip)
        )

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
    def _fetch_modules(
        file_paths: Iterable["os.PathLike"],
    ) -> Iterable["types.ModuleType"]:
        """
        Get all modules from an iterable of file paths.

        Parameters
        ----------
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
            module_name = path.stem  # type: ignore
            if module_name in sys.modules:
                # TODO:
                # Do we ever reach here?
                print(f"Skiping already loaded module {module_name}")
                continue

            module_spec = importlib.util.spec_from_file_location(module_name, path)
            module = importlib.util.module_from_spec(module_spec)  # type: ignore
            module_spec.loader.exec_module(module)  # type: ignore
            yield module

    @staticmethod
    def iter_dir(
        path: "os.PathLike",
        *,
        skip: Optional[Union[Sequence[str], Set[str], FrozenSet[str]]],
    ) -> Iterable["os.PathLike"]:
        """
        Iterating over a directory, skipping specified file names.

        Parameters
        ----------
        path : :class:`os.PathLike`
            Path of the direcory to iterate over.
        skip : Union[Sequence[str], Set[str], FrozenSet[str]], optional
            File names to skip.

        Yields
        ------
        :class:`os.PathLike`
            File paths that have not got skipped over.
        """
        # TODO(maybe): Add recursive for dirs?
        for child in path.iterdir():  # type: ignore
            if child.is_dir():
                continue
            if child.stem in skip:  # type: ignore
                continue
            if child.suffix not in SOURCE_SUFFIXES:
                continue
            yield child

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
