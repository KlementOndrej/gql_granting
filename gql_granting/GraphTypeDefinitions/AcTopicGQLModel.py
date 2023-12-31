import strawberry
import uuid
import typing
import datetime
import logging
import asyncio
from uuid import UUID
from typing import Optional, List, Union, Annotated

from ..utils.Dataloaders import getLoadersFromInfo, getUserFromInfo
from .BaseGQLModel import BaseGQLModel

#from .AcSemesterGQLModel import AcSemesterGQLModel
#from .AcLessonGQLModel import AcLessonGQLModel

AcSemesterGQLModel= Annotated["AcSemesterGQLModel",strawberry.lazy(".AcSemesterGQLModel")]
AcLessonGQLModel= Annotated["AcLessonGQLModel",strawberry.lazy(".AcLessonGQLModel")]

@strawberry.federation.type(
    keys=["id"],
    description="""Entity which represents a theme included in semester of subject""",
)
class AcTopicGQLModel:
    @classmethod
    def getLoader(cls, info):
        loader = getLoadersFromInfo(info).topics
        return loader

    @strawberry.field(description="""primary key""")
    def id(self) -> UUID:
        return self.id

    @strawberry.field(description="""name ("Introduction")""")
    def name(self) -> str:
        return self.name

    @strawberry.field(description="""english name ("Introduction")""")
    def name_en(self) -> str:
        return self.name_en

    @strawberry.field(description="""datetime lastchange""")
    def lastchange(self) -> str:
        return self.lastchange

    @strawberry.field(description="""order (1)""")
    def order(self) -> Union[int, None]:
        return self.order

    @strawberry.field(description="""Semester of subject which owns the topic""")
    async def semester(self, info: strawberry.types.Info) -> Optional["AcSemesterGQLModel"]:
        from .AcSemesterGQLModel import AcSemesterGQLModel  
        result = await AcSemesterGQLModel.resolve_reference(info, self.semester_id)
        return result

    @strawberry.field(description="""Lessons for a topic""")
    async def lessons(self, info: strawberry.types.Info) -> List["AcLessonGQLModel"]:
        loader = getLoaders(info).lessons
        result = await loader.filter_by(topic_id=self.id)
        return result

#################################################
#
# Special fields for query
#
#################################################
@strawberry.field(description="""Finds a topic by its id""")
async def actopic_by_id(
        self, info: strawberry.types.Info, id: UUID
    ) -> Union["AcTopicGQLModel", None]:
        result = await AcTopicGQLModel.resolve_reference(info, id)
        return result


#################################################
#
# Special fields for mutation
#
#################################################

@strawberry.input
class TopicInsertGQLModel:
    semester_id: UUID
    order: Optional[int] = 0
    name: Optional[str] = "New Topic"
    name_en: Optional[str] = "New Topic"
    id: Optional[UUID] = None

@strawberry.input
class TopicUpdateGQLModel:
    id: UUID
    lastchange: datetime.datetime
    order: Optional[int] = None
    name: Optional[str] = None
    name_en: Optional[str] = None

@strawberry.type
class TopicResultGQLModel:
    id: UUID = None
    msg: str = None

    @strawberry.field(description="""Result of topic operation""")
    async def topic(self, info: strawberry.types.Info) -> Union[AcTopicGQLModel, None]:
        result = await AcTopicGQLModel.resolve_reference(info, self.id)
        return result

@strawberry.mutation(description="""Adds new study topic""")
async def topic_insert(self, info: strawberry.types.Info, topic: TopicInsertGQLModel) -> TopicResultGQLModel:
        loader = getLoaders(info).topics
        row = await loader.insert(topic)
        result = TopicResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        return result

@strawberry.mutation(description="""Update the study topic""")
async def topic_update(self, info: strawberry.types.Info, topic: TopicUpdateGQLModel) -> TopicResultGQLModel:
        loader = getLoaders(info).topics
        row = await loader.update(topic)
        result = TopicResultGQLModel()
        result.msg = "ok"
        result.id = topic.id
        if row is None:
            result.msg = "fail"
            
        return result