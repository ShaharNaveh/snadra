import argparse
import enum
import functools
from typing import Dict, Set

import pygments.token as ptoken


class Complete(enum.Enum):
    """
    Command arguments, completion options.

    Attributes
    ----------
    CHOICES : enum.auto
        Complete argument from the list of choices specified in `parameter`.
    NONE : enum.auto
        Do not provide argument completions.
    """

    CHOICES = enum.auto()
    NONE = enum.auto()


class Parameter:
    """
    Representation of a parameter for the command parsing.

    Attributes
    ----------
    complete : snadra._core.base.Complete
    token : pygments:token.Name.Label
    group : str, optional
    """

    def __init__(
        self,
        complete: Complete,
        token=ptoken.Name.Label,
        *args,
        **kwargs,
    ) -> None:
        self.complete = complete
        self.token = token
        self.args = args
        self.kwargs = kwargs


class CommandDefinition:
    """
    The generic structure for commands.

    Attributes
    ----------
    keywords : set of str
        Set of the keywords for the new command.
    description : str
        Help text for the new command.
    long_help : str
        Long help for the command.
    arguments : Dict[str, snadra._core.base.Parameter]
        Dictionary of parameter definitions created with the :class:`Parameter` class.
        If this is None, your command will receive the
        raw argument string and no processing will be done except
        removing the leading command name.
    """

    keywords: Set[str] = {"unimplemented"}
    description: str = ""
    long_help: str = ""
    arguments: Dict[str, Parameter] = {}
    defaults: Dict = {}

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

    def run(self, args: argparse.Namespace):
        """
        This is what gets run for each command.

        Parameters
        ----------
        args : argparse.Namespace
            Namespace containing the parsed arguments.

        Raises
        ------
        NotImplementedError
            If there was no :meth:`snadra._core.base.CommandDefinition.run`
            method for the new command's class.
        """
        raise NotImplementedError

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
