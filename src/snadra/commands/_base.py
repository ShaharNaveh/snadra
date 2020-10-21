"""
foo bar baz
"""
import argparse
import enum
import functools
import typing


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
        self, complete: Complete, group: typing.Optional[str], *args, **kwargs
    ) -> None:
        self.complete = complete
        self.group = group
        self.args = args
        self.kwargs = kwargs


class CommandDefinition:
    KEYWORDS: typing.List[str] = ["unimplemented"]
    HELP_TEXT: str = ""
    ARGS: typing.Dict[str, Parameter] = {}
    GROUPS: typing.Dict[str, Group] = {}
    DEFAULTS: typing.Dict = {}

    def __init__(self):
        """
        Initialize a new command instance. Parse the local arguments array
        into an argparse object.
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

    def run(self, args):
        """
        This is the "main" for your new command. This should perform the action
        represented by your command.

        :param args: the argparse Namespace containing your parsed arguments
        """
        raise NotImplementedError

    def build_parser(
        self,
        parser: argparse.ArgumentParser,
        args: typing.Dict[str, Parameter],
        group_defs: typing.Dict[str, Group],
    ):
        """
        Parse the ARGS and DEFAULTS dictionaries to build an argparse ArgumentParser
        for this command. You should not need to overload this.

        :param parser: the parser object to add arguments to
        :param args: the ARGS dictionary
        """

        groups: typing.Dict = {}
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
