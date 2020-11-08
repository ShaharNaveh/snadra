:mod:`snadra.commands.help`
===========================

.. py:module:: snadra.commands.help


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   snadra.commands.help.Command



.. py:class:: Command

   Bases: :class:`snadra._core.base.CommandDefinition`

   The command `help`, for displaying help information about other commands.

   .. attribute:: ARGS
      

      

   .. attribute:: DESCRIPTION
      :annotation: = List all known commands and print their help message

      

   .. attribute:: KEYWORDS
      

      

   .. attribute:: LONG_HELP
      :annotation: = THE LONG HELP MESSAGE OF 'help'

      

   .. attribute:: _commands
      

      

   .. attribute:: _core_commands_keywords
      

      

   .. attribute:: available_keywords
      

      

   .. method:: run(self, args: argparse.Namespace)

      Show the help.

      :param args: The arguments for the command.
      :type args: :class:`argparse.Namespace`



