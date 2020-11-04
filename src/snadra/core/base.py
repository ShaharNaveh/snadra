import argparse
import enum
import functools
import pkgutil
from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Optional, Set, Union

import pygments.token as ptoken

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

    def __init__(self, mutex: bool = False, **kwargs) -> None:
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
    ARGS: Optional[Dict[str, Parameter]] = {}
    GROUPS: Dict[str, Group] = {}
    DEFAULTS: Dict = {}

    def __init__(self) -> None:
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
            self.parser = None  # type: ignore

    def __key(self) -> str:
        """
        The unique identifier of the command.

        Returns
        -------
        str
            The unique identifier of the command.

        Notes
        -----
        Since we have a test case that validate that there are no
        duplicate keywords, this *should* be safe, maybe, hopefully.
        """
        return "".join(sorted(self.KEYWORDS))

    def __hash__(self) -> int:
        return hash(self.__key())

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, CommandDefinition):
            return self.__key() == other.__key()
        return NotImplemented

    def run(self, args: argparse.Namespace):
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
        args : Dict[str, Parameter]
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

    def __init__(
        self,
        *,
        command_dirs: Union[str, List[str]],
        ignore: Optional[Union[str, Iterable[str]]] = None,
    ) -> None:
        """
        Get all the commands from the specified directories.

        Parameters
        ----------
        command_dirs : Union[str, List[str]]
            List containing string representation of paths to the command directories.
        ignore : Set[str], optional
            The module names to ignore.
        """
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
        Dict[str, CommandDefinition]
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
        SourceFileLoader
        """
        if ignore is None:
            ignore = set()

        for loader, module_name, _ in pkgutil.walk_packages(path_list):
            if module_name in ignore:
                continue
            yield loader.find_module(module_name)
