:mod:`snadra._core.parsers`
===========================

.. py:module:: snadra._core.parsers


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   snadra._core.parsers.CommandParser



.. py:class:: CommandParser

   Responsible for handling the commands entered.

   Maps each command and it's arguments to the desired action.

   .. method:: _parse_line(line: str) -> Optional[Tuple[List[str], str]]
      :staticmethod:

      :param line: The full command (including arguments).
      :type line: str

      :returns: Tuple with the line as a list.
                and the parsed line.
      :rtype: Optional[Tuple[List[str], str]]

      :raises ValueError: If could not parse the line correctly.

      .. rubric:: Examples

      >>> line = "command --target 127.0.0.1 --port 80"
      >>> CommandParser._parse_line(line)
      (['command', '--target', '127.0.0.1', '--port', '80'], 'command --target 127.0.0.1 --port 80')


   .. method:: dispatch_line(self, line: str) -> None

      Execute each command that was entered to the console.

      :param line: The full command (including arguments) as a string.
      :type line: str


   .. method:: run(self) -> None

      The main loop.

      This is an infitine loop, until the user decides to exit.


   .. method:: setup_prompt(self)

      See Notes section.

      .. rubric:: Notes

      The only reason for this being in a seperate function is that it changes
      the `sys.stdout` and `sys.stderr` which disturbes `pytest`.



