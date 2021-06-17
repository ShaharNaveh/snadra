from typing import TYPE_CHECKING

from sqlalchemy.future import select

from _snadra.cmd.utils import console
from _snadra.db.config import Base, async_session
from _snadra.db.models import Workspace

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.ext.asyncio.engine import AsyncEngine


async def start_db(engine: "AsyncEngine"):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def insert_default_rows(session: "AsyncSession") -> None:

    async with async_session() as session:
        async with session.begin():
            stmt = select(Workspace).where(Workspace.name == "default")
            result = await session.execute(stmt)
            workspace = result.scalar_one_or_none()

            if not workspace:
                default_workspace = Workspace(
                    name="default", description="Default workspace"
                )
                session.add(default_workspace)
                await session.commit()
            else:
                console.log("Found default workspace, skipping")
