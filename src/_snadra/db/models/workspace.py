from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.sql import func

from _snadra.db.config import Base


class Workspace(Base):  # type: ignore
    __tablename__ = "workspaces"

    name = Column(Text, primary_key=True, nullable=False)
    description = Column(String(length=4096), nullable=False, server_default="")
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    __mapper_args__ = {"eager_defaults": True}
