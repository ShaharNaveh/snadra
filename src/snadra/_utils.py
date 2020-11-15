import abc
import argparse
import functools
from typing import Dict, Set

from rich.console import Console

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

    def __init__(self) -> None:
        # Create the parser object
        if self.arguments is not None:
            for keyword in self.keywords:
                self.parser = argparse.ArgumentParser(
                    prog=keyword,
                    description=self.description,
                    formatter_class=argparse.RawDescriptionHelpFormatter,
                )
                self.build_parser(self.parser, self.arguments)
        else:
            self.parser = None  # type: ignore

    def build_parser(
        self,
        parser: argparse.ArgumentParser,
        args: Dict[str, Parameter],
    ) -> None:
        """
        Parse the ARGS and DEFAULTS dictionaries to build an argparse ArgumentParser
        for this command. You should not need to overload this.

        Parameters
        ----------
        parser : argparse.ArgumentParser
            Parser object to add arguments to.
        args : Dict[str, snadra._core.base.Parameter]
            `ARGS` dictionary.
        """
        for arg, param in args.items():
            names = arg.split(",")
            group = parser

            # Patch choice to work with a callable
            if "choices" in param.kwargs and callable(param.kwargs["choices"]):
                method = param.kwargs["choices"]

                class wrapper:
                    def __init__(wself, method) -> None:
                        wself.method = method

                    def __iter__(wself):
                        yield from wself.method(self)

                param.kwargs["choices"] = wrapper(method)

            # Patch "type" so we can see "self"
            if (
                "type" in param.kwargs
                and isinstance(param.kwargs["type"], tuple)
                and param.kwargs["type"][0] == "method"
            ):
                param.kwargs["type"] = functools.partial(param.kwargs["type"][1], self)

            group.add_argument(*names, *param.args, **param.kwargs)

        parser.set_defaults(**self.defaults)

    @property
    def defaults(self):
        """
        foo bar baz.
        """
        return {}

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
    def run(self, args: argparse.Namespace) -> None:
        """
        Implementation for the new command.

        This is responsible for the actual action of the command.
        """
        ...
