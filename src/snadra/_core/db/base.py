from typing import TYPE_CHECKING

from snadra._core.db.config import Base

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio.engine import AsyncEngine


async def start_db(engine: "AsyncEngine"):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
