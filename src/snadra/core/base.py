import argparse
import enum
import functools
import pkgutil
from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Optional, Set, Tuple

import pygments.token as ptoken

import snadra._utils as snutils

if TYPE_CHECKING:
    from importlib.machinery import SourceFileLoader


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


'''
def parameter(complete, token=ptoken.Name.Label, *args, **kwargs):
    """
    foo bar baz
    """
    return (complete, token, args, kwargs)
'''


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

    def __hash__(self) -> int:
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


class Commands:
    """
    Holds all the relevant commands attributes.
    """

    def __init__(self) -> None:
        self._commands_dict = self._refresh_command_dict()

    def _refresh_command_dict(self) -> Dict[str, "CommandDefinition"]:
        """
        foo bar baz
        """
        commands_dict: Dict[str, "CommandDefinition"] = {}
        commands_dir = [snutils.get_commands_dir()]

        for module in Commands.find_modules(commands_dir, to_ignore={"_base"}):  # type: ignore # noqa: E501
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
        CommandDefinition, or None
            The command that is mapped to `keyword`, if `keyword` is not mapped to any
            command, `None` is returned.
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
    def available_commands(self) -> Set["CommandDefinition"]:
        """
        Get all the available keywords.

        Returns
        -------
        Set[CommandDefinition]
            All the available commands.
        """
        return set(self._commands_dict.values())

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
    def find_modules(
        path: List[str], *, to_ignore: Optional[Set[str]] = None
    ) -> Iterable["SourceFileLoader"]:
        """
        Find modules in a given path.

        Parameters
        ----------
        path : List[str]
            Path where to find the modules.
        to_ignore : Set[str], optional
            Set of module names to ignore.

        Yields
        ------
        SourceFileLoader
        """
        if to_ignore is None:
            to_ignore = set()

        for loader, module_name, _ in pkgutil.walk_packages(path):
            if module_name in to_ignore:
                continue
            yield loader.find_module(module_name)
