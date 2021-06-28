"""
Manage workspaces.
"""
from typing import TYPE_CHECKING

from rich import box as rich_box
from rich.table import Table as RichTable
from sqlalchemy import delete
from sqlalchemy.future import select

from _snadra.cmd import CommandMeta
from _snadra.cmd.utils import console
from _snadra.db.config import async_session
from _snadra.db.models import Workspace
from _snadra.state import state

if TYPE_CHECKING:
    import argparse

    from sqlalchemy.engine.result import ChunkedIteratorResult
    from sqlalchemy.ext.asyncio import AsyncSession


class Command(CommandMeta):
    """
    Help message for "workspace".
    """

    keyword = "workspace"
    aliases = {"workspaces"}
    description = "Manage workspaces"
    long_help = "LONG HELP FOR WORKSPACE COMMAND"

    arguments = {
        "target": {"help": "Target workspace", "metavar": "target", "nargs": "?"},
        "-a,--add": {"action": "store_true", "help": "Add a workspace"},
        "-d,--delete": {"action": "store_true", "help": "Delete a workspace"},
        "--desc,--description": {"help": "Description for the workspace"},
    }

    @staticmethod
    async def is_workspace_exists(
        target: str, *, async_session: "AsyncSession"
    ) -> bool:
        async with async_session() as session:
            async with session.begin():
                stmt = select(Workspace).where(Workspace.name == target)
                result = await session.execute(stmt)
        workspace = result.scalar_one_or_none()

        return bool(workspace)

    @staticmethod
    async def add_workspace(
        target: str, desc: str, *, async_session: "AsyncSession"
    ) -> None:
        async with async_session() as session:
            async with session.begin():
                workspace = Workspace(name=target, description=desc)
                session.add(workspace)
                await session.commit()

    @staticmethod
    async def delete_workspace(target: str, *, async_session: "AsyncSession") -> None:
        async with async_session() as session:
            async with session.begin():
                stmt = delete(Workspace).where(Workspace.name == target)
                await session.execute(stmt)

    @staticmethod
    async def all_workspaces(
        *, async_session: "AsyncSession"
    ) -> "ChunkedIteratorResult":
        async with async_session() as session:
            async with session.begin():
                stmt = select(Workspace)
                result = await session.execute(stmt)

        return result

    @staticmethod
    def workspace_table(workspaces: "ChunkedIteratorResult") -> RichTable:
        # TODO:
        # Have this with cache
        table = RichTable(title="Workspaces", box=rich_box.SIMPLE)
        table.add_column("Name")
        table.add_column("Description")
        table.add_column("Created at")
        table.add_column("Updated at")

        for workspace_metadata in workspaces.scalars():
            name = workspace_metadata.name
            description = workspace_metadata.description
            created_at = workspace_metadata.created_at.strftime("%d/%m/%Y, %H:%M:%S")
            updated_at = workspace_metadata.updated_at
            updated_at = workspace_metadata.updated_at
            if updated_at is None:
                updated_at = "#"
            else:
                updated_at = updated_at.strftime("%d/%m/%Y, %H:%M:%S")

            table.add_row(name, description, created_at, updated_at)

        return table

    async def run(self, args: "argparse.Namespace") -> None:
        """
        Manage workspaces.

        Parameters
        ----------
        args : :class:`argparse.Namespace`
            The arguments for the command.
        """
        target = args.target
        do_add = args.add
        do_delete = args.delete

        if do_add and do_delete:
            # Error: conflicting flags
            console.log("[red]Error[/red]: Conflicting flags 'add' and 'delete'")

        if target is not None:
            is_exists = await self.is_workspace_exists(
                target=target, async_session=async_session
            )
            if do_add:
                # Add workspace
                if is_exists:
                    console.log("Workspace already exists!")
                    return
                await Command.add_workspace(
                    target=target, desc=args.desc, async_session=async_session
                )
            elif do_delete:
                # Delete workspace
                if not is_exists:
                    console.log(
                        f"[red]Error[/red]: Workspace {repr(target)} does not exists!"
                    )
                    return
                await Command.delete_workspace(
                    target=target, async_session=async_session
                )
            else:
                # Switch to workspace
                if not is_exists:
                    console.log(
                        f"[red]Error[/red]: Workspace {repr(target)} does not exists!"
                    )
                    return
                state["current_workspace"] = target
        else:
            if do_add:
                # Error: missing argument
                console.log("Missing argument 'target'")
                return
            elif do_delete:
                # Error: missing argument
                console.log("Missing argument 'target'")
                return
            else:
                # Show workspaces
                workspaces = await Command.all_workspaces(async_session=async_session)

                table = Command.workspace_table(workspaces=workspaces)
                console.print(table)
                return
