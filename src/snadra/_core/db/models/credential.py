from sqlalchemy import Column, Integer, Sequence, String, Text

from snadra._core.db.config import Base


class Credential(Base):
    __tablename__ = "credentials"
    id = Column(Integer, Sequence("credential_id_seq"), primary_key=True)
    credtype = Column(String(255))
    domain = Column(Text)
    username = Column(Text)
    password = Column(Text)
    host = Column(Text)
    os = Column(String(255))
    sid = Column(String(255))
    notes = Column(Text)
