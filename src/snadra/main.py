"""
foo bar baz
"""
import cmd
import os


class Console(cmd.Cmd):
    """
    foo bar baz
    """

    prompt = "snadra> "

    def __init__(self: "Console"):
        super().__init__()

    def do_exit(self: "Console", line: str) -> bool:
        """
        Exit the shell.

        Parameters
        ----------
        self : snadra.Console
        line: str
            Arguments that comes after the command, in this case None.

        Returns
        -------
        bool
            True when ever you call this command.
        """
        return True

    def do_pwd(self: "Console", line: str) -> None:
        """
        Print the current working directory.

        Parameters
        ----------
        self: snadra.Console
        line: str
            Arguments that comes after the command.

        """
        current_working_directory = os.getcwd()
        print(current_working_directory)

    def do_quit(self: "Console", line: str) -> bool:
        """
        Exit the shell.

        Parameters
        ----------
        self : snadra.Console
        line: str
            Arguments that comes after the command, in this case None.

        Returns
        -------
        bool
            True when ever you call this command.
        """
        return True


if __name__ == "__main__":
    Console().cmdloop()
