:mod:`snadra._core.base`
========================

.. py:module:: snadra._core.base


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   snadra._core.base.CommandDefinition
   snadra._core.base.Commands
   snadra._core.base.Complete
   snadra._core.base.Group
   snadra._core.base.Parameter



.. py:class:: CommandDefinition

   THe generic structure for commands.

   .. attribute:: KEYWORDS

      Set of the keywords for the new command.

      :type: Set[str]

   .. attribute:: DESCRIPTION

      Help text for the new command.

      :type: str

   .. attribute:: LONG_HELP

      Long help for the command.

      :type: str

   .. attribute:: ARGS

      Dictionary of parameter definitions created with the :class:`Parameter` class.
      If this is None, your command will receive the
      raw argument string and no processing will be done except
      removing the leading command name.

      :type: Dict[str, :class:`Parameter`]

   .. attribute:: GROUPS

      Dictionary mapping group definitions to group names.
      The parameters to Group are passed directly to either
      add_argument_group or add_mutually_exclusive_group with the exception of the
      mutex arg, which determines the group type.

      :type: Dict[str, :class:`Group`]

   .. attribute:: ARGS
      :annotation: :Dict[str, Parameter]

      

   .. attribute:: DEFAULTS
      :annotation: :Dict

      

   .. attribute:: DESCRIPTION
      :annotation: :str = 

      

   .. attribute:: GROUPS
      :annotation: :Dict[str, Group]

      

   .. attribute:: KEYWORDS
      :annotation: :Set[str]

      

   .. attribute:: LONG_HELP
      :annotation: :str = 

      

   .. method:: __eq__(self, other: Any) -> bool

      Return self==value.


   .. method:: __hash__(self) -> int

      Return hash(self).


   .. method:: __key(self) -> str

      The unique identifier of the command.

      :returns: The unique identifier of the command.
      :rtype: str

      .. rubric:: Notes

      Since we have a test case that validate that there are no
      duplicate keywords, this *should* be safe, maybe, hopefully.


   .. method:: build_parser(self, parser: argparse.ArgumentParser, args: Dict[str, Parameter], group_defs: Dict[str, Group])

      Parse the ARGS and DEFAULTS dictionaries to build an argparse ArgumentParser
      for this command. You should not need to overload this.

      :param parser: Parser object to add arguments to.
      :type parser: :class:`argparse.ArgumentParser`
      :param args: `ARGS` dictionary.
      :type args: Dict[str, :class:`Parameter`]
      :param group_defs: :class:`Group` dictionary.
      :type group_defs: Dict[str, :class:`Group`],


   .. method:: run(self, args: argparse.Namespace)
      :abstractmethod:

      This is what gets run for each command.

      :param args: The :class:`argparse.Namespace` containing the parsed arguments.
      :type args: :class:`argparse.Namespace`

      :raises NotImplementedError: If there was no ``run`` method for the new command's class.



.. py:class:: Commands(*, command_dirs: Union[str, List[str]], ignore: Optional[Union[str, Iterable[str]]] = None)

   Holds all the relevant commands attributes.

   :param command_dirs: Sequence containing strings of paths to the command directories.
   :type command_dirs: Union[str, List[str]]
   :param ignore: The module names to ignore.
   :type ignore: Union[str, Iterable[str]], optional

   .. method:: _find_modules(path_list: List[str], *, ignore: Optional[Union[str, Iterable[str]]] = None) -> Iterable['SourceFileLoader']
      :staticmethod:

      Find modules in a given path.

      :param path: Path where to find the modules.
      :type path: List[str]
      :param ignore: Set of module names to skip.
      :type ignore: Union[str, Iterable[str]], optional

      :Yields: :class:`SourceFileLoader`


   .. method:: _refresh_command_dict(self, *, command_dirs: List[str], ignore: Optional[Union[str, Iterable[str]]] = None) -> Dict[str, 'CommandDefinition']

      Map every keyword to the desired command.

      :param command_dirs: List containing string representation of paths to the command directories.
      :type command_dirs: List[str]
      :param ignore: The module names to ignore.
      :type ignore: Union[str, Iterable[str]], optional

      :returns: Dictionary with the keywords mapped to thier command.
      :rtype: Dict[str, :class:`CommandDefinition`]


   .. method:: available_commands(self) -> Set['CommandDefinition']
      :property:

      Get all the available keywords.

      :returns: All the available commands.
      :rtype: Set[:class:`CommandDefinition`]


   .. method:: get_command(self, keyword: str) -> Optional['CommandDefinition']

      Get the command that mapped to a keyword.

      :param keyword: Keyword to check.
      :type keyword: str

      :returns: The command that is mapped to ``keyword``,
                if ``keyword`` is not mapped to any command, `None` is returned.
      :rtype: Optional[:class:`CommandDefinition`]


   .. method:: is_valid_keyword(self, keyword: str) -> bool

      Check if a given keyword is mapped to a valid command.

      :param keyword: Keyword to check.
      :type keyword: str

      :returns: Whether or not the keyword is mapped to a valid command.
      :rtype: bool


   .. method:: keywords(self) -> Set[str]
      :property:

      Get all the available keywords.

      :returns: All the available keywords.
      :rtype: Set[str]



.. py:class:: Complete

   Bases: :class:`enum.Enum`

   Command arguments, completion options.

   .. attribute:: CHOICES

      Complete argument from the list of choices specified in ``parameter``.

      :type: :class:`enum.auto`

   .. attribute:: NONE

      Do not provide argument completions.

      :type: :class:`enum.auto`

   .. attribute:: CHOICES
      

      

   .. attribute:: NONE
      

      


.. py:class:: Group(mutex: bool = False, **kwargs)

   This just wraps the parameters to the
   add_argument_group and add_mutually_exclusive_group


.. py:class:: Parameter(complete: Complete, token=ptoken.Name.Label, group: Optional[str] = None, *args, **kwargs)


