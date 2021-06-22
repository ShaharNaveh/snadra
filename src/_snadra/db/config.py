from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# TODO: Integrate with the config system
__db_user = "snadra"
__db_password = "snadra"
__db_host = "127.0.0.1"
__db_database = "snadra"
engine = create_async_engine(
    f"postgresql+asyncpg://{__db_user}:{__db_password}@{__db_host}/{__db_database}",
    echo=False,
    future=True,
)


async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()
