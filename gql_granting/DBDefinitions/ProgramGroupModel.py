import sqlalchemy
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table, Boolean, Float, DECIMAL
from .base import BaseModel
from .uuid import UUIDColumn, UUIDFKey

class ProgramGroupModel(BaseModel):
    """Program group

    Args:
        id (ID): An primary key.
        program_id:
        ac_id:
        group_id:
    """
    __tablename__ = "acprogramgroups"
    program_id = Column(ForeignKey("acprograms.id"))
    id = UUIDColumn()
    ac_id = (
        UUIDColumn()
    )  # can be a program, also can be a subject, this row can be in a table only once per program and once per subject
    group_id = UUIDFKey()#Column(ForeignKey("groups.id"))