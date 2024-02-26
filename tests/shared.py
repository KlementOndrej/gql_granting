import sqlalchemy
import sys
import asyncio
import logging
# setting path

import pytest

# from ..uoishelpers.uuid import UUIDColumn

from DBDefinitions import BaseModel
from DBDefinitions import ProgramModel, ProgramLevelTypeModel, ProgramFormTypeModel, ProgramLanguageTypeModel, ProgramTitleTypeModel, ProgramTypeModel
from DBDefinitions import SemesterModel, SubjectModel, TopicModel, LessonModel, LessonTypeModel
from DBDefinitions import ClassificationLevelModel, ClassificationModel, ClassificationTypeModel

async def prepare_in_memory_sqllite():
    from sqlalchemy.ext.asyncio import create_async_engine
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm import sessionmaker

    asyncEngine = create_async_engine("sqlite+aiosqlite:///:memory:")
    # asyncEngine = create_async_engine("sqlite+aiosqlite:///data.sqlite")
    async with asyncEngine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    async_session_maker = sessionmaker(
        asyncEngine, expire_on_commit=False, class_=AsyncSession
    )

    return async_session_maker

from utils.DBFeeder import get_demodata

async def prepare_demodata(async_session_maker):
    data = get_demodata()

    from uoishelpers.feeders import ImportModels

    await ImportModels(
        async_session_maker,
        [           
            ProgramModel, ProgramLevelTypeModel, ProgramFormTypeModel, ProgramLanguageTypeModel, ProgramTitleTypeModel, ProgramTypeModel,
            SemesterModel, SubjectModel, TopicModel, LessonModel, LessonTypeModel,
            ClassificationLevelModel, ClassificationModel, ClassificationTypeModel        
        ],
        data,
    )


from utils.Dataloaders import  createLoaders


def createContext(asyncSessionMaker):
    return {
        "asyncSessionMaker": asyncSessionMaker,
        "all": createLoaders(asyncSessionMaker),
    }

from GraphTypeDefinitions import schema

def CreateSchemaFunction():
    async def result(query, variables={}):

        async_session_maker = await prepare_in_memory_sqllite()
        await prepare_demodata(async_session_maker)
        context_value = createContext(async_session_maker)
        logging.debug(f"query for {query} with {variables}")
        print(f"query for {query} with {variables}")
        resp = await schema.execute(
            query=query, 
            variable_values=variables, 
            context_value=context_value
        )

        assert resp.errors is None
        respdata = resp.data
        logging.debug(f"response: {respdata}")

        result = {"data": respdata, "errors": resp.errors}
        return result

    return result