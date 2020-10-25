"""
foo bar baz
"""
import argparse
import enum
import functools
from typing import Any, Dict, List, Optional, Set, Tuple

import pygments.token as ptoken


class Complete(enum.Enum):
    """
    Command arguments, completion options.

    Attributes
    ----------
    CHOICES : enum.auto
        Complete argument from the list of choices specified in ``parameter``.
    NONE : enum.auto
        Do not provide argument completions.
    """

    CHOICES = enum.auto()
    NONE = enum.auto()


class Group:
    """
    This just wraps the parameters to the
    add_argument_group and add_mutually_exclusive_group
    """

    def __init__(self, mutex: bool = False, **kwargs):
        self.mutex = mutex
        self.kwargs = kwargs


class Parameter:
    def __init__(
        self,
        complete: Complete,
        token=ptoken.Name.Label,
        group: Optional[str] = None,
        *args,
        **kwargs,
    ) -> None:
        self.complete = complete
        self.token = token
        self.group = group
        self.args = args
        self.kwargs = kwargs


def parameter(complete, token=ptoken.Name.Label, *args, **kwargs):
    """
    foo bar baz
    """
    return (complete, token, args, kwargs)


class CommandDefinition:
    """
    THe generic structure for commands.

    Attributes
    ----------
    KEYWORDS : Set[str]
        Set of the keywords for the new command.

    HELP_TEXT : str
        Help text for the new command.

    ARGS : Dict[str, ``Parameter``]
        Dictionary of parameter definitions created with the ``Parameter`` class.
        If this is None, your command will receive the
        raw argument string and no processing will be done except
        removing the leading command name.

    GROUPS : Dict[str, ``Group``]
        Dictionary mapping group definitions to group names.
        The parameters to Group are passed directly to either
        add_argument_group or add_mutually_exclusive_group with the exception of the
        mutex arg, which determines the group type.
    """

    KEYWORDS: Set[str] = {"unimplemented"}
    HELP_TEXT: str = ""
    ARGS: Dict[str, Optional[Parameter]] = {}
    GROUPS: Dict[str, Group] = {}
    DEFAULTS: Dict = {}

    def __init__(self):
        """
        Initialize new command instance.

        Parses the `ARGS` dictionary into an argparse object.
        """
        # Create the parser object
        if self.ARGS is not None:
            for keyword in self.KEYWORDS:
                self.parser = argparse.ArgumentParser(
                    prog=keyword,
                    description=self.HELP_TEXT,
                    formatter_class=argparse.RawDescriptionHelpFormatter,
                )
                self.build_parser(self.parser, self.ARGS, self.GROUPS)
        else:
            self.parser = None

    def __key(self) -> Tuple[str, str]:
        keywords = "".join(sorted(self.KEYWORDS))
        return (keywords, self.HELP_TEXT)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, CommandDefinition):
            return self.__key() == other.__key()
        return NotImplemented

    def run(self, args):
        """
        This is what gets run for each command.

        Parameters
        ----------
        args : argparse.Namespace
            The `argparse.Namespace` containing the parsed arguments.

        Raises
        ------
        NotImplementedError
            If there was not `run` method for the new command's class.
        """
        raise NotImplementedError

    def build_parser(
        self,
        parser: argparse.ArgumentParser,
        args: Dict[str, Parameter],
        group_defs: Dict[str, Group],
    ):
        """
        Parse the ARGS and DEFAULTS dictionaries to build an argparse ArgumentParser
        for this command. You should not need to overload this.

        :param args: the ARGS dictionary

        Parameters
        ----------
        parser : argparse.ArgumentParser
            Parser object to add arguments to.
        args : Dict[str, Optional[Parameter]]
            ``ARGS`` dictionary.
        group_defs : Dict[str, ``Group``],
            ``Group`` dictionary.
        """
        groups: Dict = {}
        for name, definition in group_defs.items():
            if definition.mutex:
                groups[name] = parser.add_mutually_exclusive_group(**definition.kwargs)
            else:
                groups[name] = parser.add_argument_group(**definition.kwargs)

        for arg, param in args.items():
            names = arg.split(",")

            if param.group is not None and param.group not in groups:
                raise ValueError(f"{param.group}: no such group")

            if param.group is not None:
                group = groups[param.group]
            else:
                group = parser

            # Patch choice to work with a callable
            if "choices" in param.kwargs and callable(param.kwargs["choices"]):
                method = param.kwargs["choices"]

                class wrapper:
                    def __init__(wself, method):
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

        parser.set_defaults(**self.DEFAULTS)
