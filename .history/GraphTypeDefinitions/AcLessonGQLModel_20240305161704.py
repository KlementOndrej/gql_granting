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

AcTopicGQLModel = typing.Annotated["AcTopicGQLModel",strawberry.lazy(".AcTopicGQLModel")]
AcLessonTypeGQLModel = typing.Annotated["AcLessonTypeGQLModel",strawberry.lazy(".AcLessonTypeGQLModel")]

@strawberry.federation.type(
    keys=["id"],
    description="""Entity which represents single lesson included in a topic""",
)
class AcLessonGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        loader = getLoadersFromInfo(info).lessons
        return loader

    id = resolve_id
    lastchange = resolve_lastchange

    @strawberry.field(description="""Lesson type""")
    async def lesson_type(self, info: strawberry.types.Info) -> typing.Optional["AcLessonTypeGQLModel"]:
        from .AcLessonTypeGQLModel import AcLessonTypeGQLModel
        result = await AcLessonTypeGQLModel.resolve_reference(info, self.type_id)
        return result

    @strawberry.field(description="""Number of hour of this lesson in the topic""")
    def count(self) -> int:
        return self.count

    @strawberry.field(description="""The topic which owns this lesson""")
    async def topic(self, info: strawberry.types.Info) -> typing.Optional["AcTopicGQLModel"]:
        from .AcTopicGQLModel import AcTopicGQLModel
        result = await AcTopicGQLModel.resolve_reference(info, self.topic_id)
        return result

#################################################
# Query
#################################################

from dataclasses import dataclass 
from uoishelpers.resolvers import createInputs

@createInputs 
@dataclass 
class LessonWhereFilter: 
   type_id : uuid.UUID 
   topic_id: uuid.UUID
   count: int

from ._GraphResolvers import asPage

@strawberry.field(
    description="""Finds a lesson by its id""",
    permission_classes=[OnlyForAuthentized()])
async def aclesson_by_id(
        self, info: strawberry.types.Info, id: uuid.UUID
    ) -> typing.Optional[AcLessonGQLModel]:
        result = await AcLessonGQLModel.resolve_reference(info, id)
        return result

@strawberry.field(
    description="""Gets all lessons""",
    permission_classes=[OnlyForAuthentized()])
@asPage
async def aclesson_page(
    self, info: strawberry.types.Info,
    where: typing.Optional[LessonWhereFilter] = None
    ) -> typing.List[AcLessonGQLModel]:
        return getLoadersFromInfo(info).lessons
    
#################################################
# Mutation
#################################################
    
@strawberry.input
class LessonInsertGQLModel:
    topic_id: uuid.UUID
    type_id: uuid.UUID = strawberry.field(description="type of the lesson")
    count: typing.Optional[int] = strawberry.field(description="count of the lessons", default=2)
    id: typing.Optional[uuid.UUID] = None

@strawberry.input
class LessonUpdateGQLModel:
    id:uuid.UUID
    lastchange: datetime.datetime
    type_id: typing.Optional[uuid.UUID] = None
    count: typing.Optional[int] = None

@strawberry.type
class LessonResultGQLModel:
    id: uuid.UUID = None
    msg: str = None

    @strawberry.field(description="""Result of topic operation""")
    async def lesson(self, info: strawberry.types.Info) -> typing.Union[AcLessonGQLModel, None]:
        result = await AcLessonGQLModel.resolve_reference(info, self.id)
        return result
    
@strawberry.mutation(
    description="""Adds new study lesson""",
    permission_classes=[OnlyForAuthentized()])
async def lesson_insert(self, info: strawberry.types.Info, lesson: LessonInsertGQLModel) -> LessonResultGQLModel:
        loader = getLoadersFromInfo(info).lessons
        row = await loader.insert(lesson)
        result = LessonResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        return result

@strawberry.mutation(
    description="""Update the study lesson""",
    permission_classes=[OnlyForAuthentized()])
async def lesson_update(self, info: strawberry.types.Info, lesson: LessonUpdateGQLModel) -> LessonResultGQLModel:
        loader = getLoadersFromInfo(info).lessons
        row = await loader.update(lesson)
        result = LessonResultGQLModel()
        result.msg = "ok"
        result.id = lesson.id
        result.msg = "ok" if (row is not None) else "fail"
            
        return result