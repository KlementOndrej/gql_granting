import strawberry
import typing
import datetime
import uuid
import logging

from utils.Dataloaders import getLoadersFromInfo, getUserFromInfo
from .BaseGQLModel import BaseGQLModel


from GraphTypeDefinitions._GraphResolvers import (
    resolve_id,
    resolve_name,
    resolve_name_en,
    resolve_changedby,
    resolve_created,
    resolve_lastchange,
    resolve_createdby,
    resolve_rbacobject,
    createRootResolver_by_id,
)
from ._GraphPermissions import RoleBasedPermission, OnlyForAuthentized


AcSemesterGQLModel = typing.Annotated["AcSemesterGQLModel",strawberry.lazy(".AcSemesterGQLModel")]
AcLessonGQLModel = typing.Annotated["AcLessonGQLModel",strawberry.lazy(".AcLessonGQLModel")]

@strawberry.federation.type(
    keys=["id"],
    description="""Entity which represents a theme included in semester of subject""",
)
class AcTopicGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        loader = getLoadersFromInfo(info).topics
        return loader
    
    id = resolve_id
    name = resolve_name
    name_en = resolve_name_en
    lastchange = resolve_lastchange

    @strawberry.field(description="""order (1)""")
    def order(self) -> typing.Union[int, None]:
        return self.order

    @strawberry.field(description="""Semester of subject which owns the topic""")
    async def semester(self, info: strawberry.types.Info) -> typing.Optional["AcSemesterGQLModel"]:
        from .AcSemesterGQLModel import AcSemesterGQLModel  
        result = await AcSemesterGQLModel.resolve_reference(info, self.semester_id)
        return result

    @strawberry.field(description="""Lessons for a topic""")
    async def lessons(self, info: strawberry.types.Info) -> typing.List["AcLessonGQLModel"]:
        loader = getLoadersFromInfo(info).lessons
        result = await loader.filter_by(topic_id=self.id)
        return result

#################################################
# Query
#################################################

from dataclasses import dataclass 
from uoishelpers.resolvers import createInputs
@createInputs
@dataclass 
class TopicWhereFilter:
    semester_id: uuid.UUID
    order: int
    name: str
    name_en: str

from ._GraphResolvers import asPage

@strawberry.field(
    description="""Finds a topic by its id""",
    permission_classes=[OnlyForAuthentized()])
async def actopic_by_id(
        self, info: strawberry.types.Info, id: uuid.UUID
    ) -> typing.Optional[AcTopicGQLModel]:
        result = await AcTopicGQLModel.resolve_reference(info, id)
        return result

@strawberry.field(
    description="""Find all topics""",
    permission_classes=[OnlyForAuthentized()])
@asPage
async def actopic_page(
        self, info: strawberry.types.Info, skip: int = 0, limit: int = 10, 
        where: typing.Optional[TopicWhereFilter] = None
    ) -> typing.List[AcTopicGQLModel]:
        return getLoadersFromInfo(info).topics

#################################################
# Mutation
#################################################

@strawberry.input
class TopicInsertGQLModel:
    semester_id: uuid.UUID
    order: typing.Optional[int] = 0
    name: typing.Optional[str] = "New Topic"
    name_en: typing.Optional[str] = "New Topic"
    id: typing.Optional[uuid.UUID] = None

@strawberry.input
class TopicUpdateGQLModel:
    id: uuid.UUID
    lastchange: datetime.datetime
    order: typing.Optional[int] = None
    name: typing.Optional[str] = None
    name_en: typing.Optional[str] = None

@strawberry.type
class TopicResultGQLModel:
    id: uuid.UUID = None
    msg: str = None

    @strawberry.field(description="""Result of topic operation""")
    async def topic(self, info: strawberry.types.Info) -> typing.Union[AcTopicGQLModel, None]:
        result = await AcTopicGQLModel.resolve_reference(info, self.id)
        return result

@strawberry.mutation(
    description="""Adds new study topic""",
    permission_classes=[OnlyForAuthentized()])
async def topic_insert(self, info: strawberry.types.Info, topic: TopicInsertGQLModel) -> TopicResultGQLModel:
        loader = getLoadersFromInfo(info).topics
        row = await loader.insert(topic)
        result = TopicResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        return result

@strawberry.mutation(
    description="""Update the study topic""",
    permission_classes=[OnlyForAuthentized()])
async def topic_update(self, info: strawberry.types.Info, topic: TopicUpdateGQLModel) -> TopicResultGQLModel:
        loader = getLoadersFromInfo(info).topics
        row = await loader.update(topic)
        result = TopicResultGQLModel()
        result.msg = "ok"
        result.id = topic.id
        result.msg = "ok" if (row is not None) else "fail"
            
        return result