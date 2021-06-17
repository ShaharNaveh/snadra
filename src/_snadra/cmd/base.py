import enum

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


# TODO:
# Make this a namedtuple.
def parameter(
    complete: Complete,
    token=ptoken.Name.Label,
    *args,
    **kwargs,
):
    """
    Representation of a parameter for the command parsing.

    Attributes
    ----------
    complete : Complete
    token : pygments:token.Name.Label
    """
    pass


class Parameter:
    """ """

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
        print(f"{self.args=}\t{self.kwargs=}")
