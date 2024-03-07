from .base import BaseModel
from .ClassificationLevelModel import ClassificationLevelModel
from .ClassificationModel import ClassificationModel
from .ClassificationTypeModel import ClassificationTypeModel
from .LessonTypeModel import LessonTypeModel
from .LessonModel import LessonModel
from .ProgramFormTypeModel import ProgramFormTypeModel
from .ProgramGroupModel import ProgramGroupModel
from .ProgramLanguageTypeModel import ProgramLanguageTypeModel
from .ProgramLevelTypeModel import ProgramLevelTypeModel
from .ProgramModel import ProgramModel
from .ProgramStudentMessages import ProgramStudentMessages
from .ProgramStudents import ProgramStudents
from .ProgramStudentStates import ProgramStudentStates
from .ProgramTitleTypeModel import ProgramTitleTypeModel
from .ProgramTypeModel import ProgramTypeModel
from .SemesterModel import SemesterModel
from .SubjectModel import SubjectModel
from .TopicModel import TopicModel
from .uuid import UUIDColumn

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine


async def startEngine(connectionstring, makeDrop=False, makeUp=True):
    """Provede nezbytne ukony a vrati asynchronni SessionMaker"""
    asyncEngine = create_async_engine(connectionstring)

    async with asyncEngine.begin() as conn:
        if makeDrop:
            await conn.run_sync(BaseModel.metadata.drop_all)
            print("BaseModel.metadata.drop_all finished")
        if makeUp:
            await conn.run_sync(BaseModel.metadata.create_all)
            print("BaseModel.metadata.create_all finished")

    async_sessionMaker = sessionmaker(
        asyncEngine, expire_on_commit=False, class_=AsyncSession
    )
    return async_sessionMaker


import os


def ComposeConnectionString():
    """Odvozuje connectionString z promennych prostredi (nebo z Docker Envs, coz je fakticky totez).
    Lze predelat na napr. konfiguracni file.
    """
    user = os.environ.get("POSTGRES_USER", "postgres")
    password = os.environ.get("POSTGRES_PASSWORD", "example")
    database = os.environ.get("POSTGRES_DB", "data")
    hostWithPort = os.environ.get("POSTGRES_HOST", "localhost:5432")

    driver = "postgresql+asyncpg"  # "postgresql+psycopg2"
    connectionstring = f"{driver}://{user}:{password}@{hostWithPort}/{database}"

    return connectionstring
