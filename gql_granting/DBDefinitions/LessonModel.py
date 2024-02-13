import sqlalchemy
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table, Boolean, Float, DECIMAL
from .base import BaseModel
from .uuid import UUIDColumn, UUIDFKey

class LessonModel(BaseModel):
    """Lesson

    Args:
        id (ID): An primary key.
        topic_id(ID): Id of the lesson topic
        type_id(ID): Id of the lesson type
        count: number of hours
    """
    __tablename__ = "aclessons"
    id = UUIDColumn()
    topic_id = Column(ForeignKey("actopics.id"), index=True)
    type_id = Column(ForeignKey("aclessontypes.id"), index=True)
    count = Column(Integer)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)

    # type = relationship('ThemeTypeModel', back_populates='items')
    # theme = relationship('StudyThemeModel', back_populates='items')
