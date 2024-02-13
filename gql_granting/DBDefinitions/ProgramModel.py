import sqlalchemy
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table, Boolean, Float, DECIMAL
from .base import BaseModel
from .uuid import UUIDColumn, UUIDFKey

class ProgramModel(BaseModel):
    """Program

    Args:
        id (ID): An primary key.
        name (str): aka Matematika
        name_en (str): aka Mathematics
        type_id (ID): structure defining the kind of program
    """
    __tablename__ = "acprograms"
    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)
    type_id = Column(ForeignKey("acprogramtypes.id"), index=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
