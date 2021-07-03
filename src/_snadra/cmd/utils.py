import abc
import argparse
from importlib.machinery import SOURCE_SUFFIXES
from typing import TYPE_CHECKING, Any, Dict, Iterable, Optional, Set

from rich.console import Console

if TYPE_CHECKING:
    import pathlib

console = Console(emoji=False)


def iter_dir(
    path: "pathlib.Path",
    include_suffixes: Optional[Iterable[str]] = None,
    skip: Optional[Set[str]] = None,
) -> Iterable["pathlib.Path"]:
    """
    Iterating over a directory, skipping specified file names.

    Parameters
    ----------
    path : pathlib.Path
        Path of the direcory to iterate over.
    include_suffixes : Iterable[str]
        Suffixes to include.
    skip : Set[str], optional
        File names to skip.

    Yields
    ------
    pathlib.Path
        File paths that have not got skipped over.
    """
    if include_suffixes is None:
        include_suffixes = SOURCE_SUFFIXES
    if skip is None:
        skip = set()

    # TODO(maybe): Add recursive for dirs?
    for child in path.iterdir():
        if child.is_dir():
            continue
        if child.stem in skip:
            continue
        if child.suffix not in include_suffixes:
            continue
        yield child


class CommandMeta(metaclass=abc.ABCMeta):
    """
    Abstract base class for command line commands.
    """

    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(
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

            parser.add_argument(*names, **param)

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
