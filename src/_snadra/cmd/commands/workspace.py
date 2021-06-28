"""
Manage workspaces.
"""
from typing import TYPE_CHECKING

from rich import box as rich_box
from rich.table import Table as RichTable
from sqlalchemy.future import select

from _snadra.cmd import CommandMeta
from _snadra.cmd.utils import console
from _snadra.db.config import async_session
from _snadra.db.models import Workspace

if TYPE_CHECKING:
    import argparse


class Command(CommandMeta):
    """
    Help message for "workspace".
    """

    keyword = "workspace"
    aliases = {"workspaces"}
    description = "Manage workspaces"
    long_help = "LONG HELP FOR WORKSPACE COMMAND"

    arguments = {
        "target": {"metavar": "target", "nargs": "?"},
        "-a,--add": {"action": "store_true", "help": "Add a workspace"},
        "-d,--delete": {"action": "store_true", "help": "Delete a workspace"},
    }

    async def is_workspace_exists(self, target: str) -> bool:
        async with async_session() as session:
            async with session.begin():
                stmt = select(Workspace).where(Workspace.name == target)
                result = await session.execute(stmt)
        workspace = result.scalar_one_or_none()

        return bool(workspace)

    async def add_workspace(self, target: str, desc: str) -> None:
        async with async_session() as session:
            async with session.begin():
                workspace = Workspace(name=target, description=desc)
                session.add(workspace)
                await session.commit()

    async def delete_workspace(self, target: str) -> None:
        pass

<<<<<<< HEAD
=======

>>>>>>> origin/ENH-add-remove-workspace
    async def run(self, args: "argparse.Namespace") -> None:
        """
        Manage workspaces.

        Parameters
        ----------
        args : :class:`argparse.Namespace`
            The arguments for the command.
        """
        target = args.target
<<<<<<< HEAD
=======
        do_add = args.add
        do_delete = args.delete





        if target is not None:
            pass
>>>>>>> origin/ENH-add-remove-workspace
        if args.action == "add":
            if target is None:
                # TODO:
                # Argparse should handle this.
<<<<<<< HEAD
                SnadraConsole().log("Missing argument 'target'")
=======
                console.log("Missing argument 'target'")
>>>>>>> origin/ENH-add-remove-workspace
                return

            is_exists = await self.is_workspace_exists(target=target)
            if is_exists:
<<<<<<< HEAD
                SnadraConsole().log("Workspace already exists!")
=======
                console.log("Workspace already exists!")
>>>>>>> origin/ENH-add-remove-workspace
                return
            else:
                await self.add_workspace(target=args.target, desc=args.description)

<<<<<<< HEAD
        SnadraConsole().log(args)
=======
        console.log(args)
>>>>>>> origin/ENH-add-remove-workspace
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

        console.print(workspace_display_table)
