import sqlalchemy
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table, Boolean, Float, DECIMAL
from .base import BaseModel
from .uuid import UUIDColumn, UUIDFKey
from sqlalchemy.orm import relationship

class ClassificationTypeModel(BaseModel):
    """Holds a particular classification type (Z, KZ, Zk, ...).

    Args:
        id (ID): An primary key.
        name (ID): Z, Zk, ...
        name_en (ID): none
    """
    __tablename__ = "acclassificationtypes"
    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)
   
    #classificationsemesters = relationship('SemesterModel', back_populates='classifications', uselist = False)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)