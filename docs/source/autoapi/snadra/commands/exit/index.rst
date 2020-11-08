:mod:`snadra.commands.exit`
===========================

.. py:module:: snadra.commands.exit

.. autoapi-nested-parse::

   The command to exit snadra.



Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   snadra.commands.exit.Command



.. py:class:: Command

   Bases: :class:`snadra._core.base.CommandDefinition`

   Help message for "exit"

   .. attribute:: ARGS
      

      

   .. attribute:: DESCRIPTION
      :annotation: = Exit the console

      

   .. attribute:: KEYWORDS
      

      

   .. attribute:: LONG_HELP
      :annotation: = LONG HELP FOR EXIT COMMAND

      

   .. method:: run(self, args: argparse.Namespace)

      Exit `snadra`.

      :param args: The arguments for the command.
      :type args: :class:`argparse.Namespace`



