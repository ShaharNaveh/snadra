"""
Manage workspaces.
"""
from typing import TYPE_CHECKING

from rich import box as rich_box
from rich.table import Table as RichTable
from sqlalchemy.future import select

from _snadra.cmd import CommandMeta, SnadraConsole
from _snadra.cmd.base import Complete, Parameter
from _snadra.db.config import async_session
from _snadra.db.models import Workspace

if TYPE_CHECKING:
    import argparse


class Command(CommandMeta):
    """
    Help message for "workspace".
    """

    keywords = {"workspace"}
    description = "Manage workspaces"
    long_help = "LONG HELP FOR WORKSPACE COMMAND"

    arguments = {
        "-a,--add": Parameter(complete=Complete.NONE, help="Add a workspace"),
        "-d,--delete": Parameter(complete=Complete.NONE, help="Delete a workspace"),
        "-s,--search": Parameter(complete=Complete.NONE, help="Search a workspace"),
    }

    async def run(self, args: "argparse.Namespace") -> None:
        """
        Manage workspaces.

        Parameters
        ----------
        args : :class:`argparse.Namespace`
            The arguments for the command.
        """
        workspace_display_table = RichTable(title="Workspaces", box=rich_box.SIMPLE)
        workspace_display_table.add_column("Name")
        workspace_display_table.add_column("Description")
        workspace_display_table.add_column("Created at")
        workspace_display_table.add_column("Updated at")

        async with async_session() as session:
            async with session.begin():
                stmt = select(Workspace)
                result = await session.execute(stmt)

        for workspace_metadata in result.scalars():
            name = workspace_metadata.name
            description = workspace_metadata.description
            created_at = workspace_metadata.created_at.strftime("%d/%m/%Y, %H:%M:%S")
            updated_at = workspace_metadata.updated_at
            updated_at = workspace_metadata.updated_at
            if updated_at is None:
                updated_at = "#"
            else:
                updated_at = updated_at.strftime("%d/%m/%Y, %H:%M:%S")

            workspace_display_table.add_row(name, description, created_at, updated_at)

        SnadraConsole().print(workspace_display_table)
