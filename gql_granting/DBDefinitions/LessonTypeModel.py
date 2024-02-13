import sqlalchemy
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table, Boolean, Float, DECIMAL
from .base import BaseModel
from .uuid import UUIDColumn, UUIDFKey

class LessonTypeModel(BaseModel):
    """Holds a particular lesson type

    Args:
        id (ID): An primary key.
        name (ID): cvičení, přednáška, ...
        name_en (ID): none
    """
    __tablename__ = "aclessontypes"
    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)
    abbr = Column(String)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    # items = relationship('StudyThemeItemModel', back_populates='type')

