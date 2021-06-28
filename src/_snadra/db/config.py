from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from _snadra.state import state

db_config = state["config"]["database"]

db_database = db_config["db"]
db_host = db_config["host"]
db_password = db_config["password"]
db_port = db_config["port"]
db_type = db_config["type"]
db_user = db_config["user"]

postgres_uri = (
    f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}"
)

if db_type == "postgres":
    engine = create_async_engine(postgres_uri, echo=False, future=True)


async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()
