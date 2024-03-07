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

AcClassificationGQLModel= typing.Annotated["AcClassificationGQLModel",strawberry.lazy(".AcClassificationGQLModel")]
AcClassificationTypeGQLModel = typing.Annotated["AcClassificationTypeGQLModel",strawberry.lazy(".AcClassificationTypeGQLModel")]
AcTopicGQLModel = typing.Annotated["AcTopicGQLModel",strawberry.lazy(".AcTopicGQLModel")]
AcSubjectGQLModel = typing.Annotated["AcSubjectGQLModel",strawberry.lazy(".AcSubjectGQLModel")]
@strawberry.federation.type(
    keys=["id"], description="""Entity representing each semester in study subject"""
)
class AcSemesterGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        loader = getLoadersFromInfo(info).semesters
        return loader

    id = resolve_id
    lastchange = resolve_lastchange

    @strawberry.field(
        description="""semester number""")
    def order(self) -> int:
        return self.order

    @strawberry.field(
        description="""credits""")
    def credits(self) -> int:
        return self.credits

    from ._GraphResolvers import asForeignList

    @strawberry.field(
        description="""Subject related to the semester (semester owner)""")
    async def classification_type(self, info: strawberry.types.Info) -> typing.Optional["AcClassificationTypeGQLModel"]:
        from .AcClassificationTypeGQLModel import AcClassificationTypeGQLModel
        result = await AcClassificationTypeGQLModel.resolve_reference(info, id = self.classificationtype_id)
        return result

    @strawberry.field(
        description="""Final classification of the semester""")
    async def classifications(self, info: strawberry.types.Info) -> typing.List["AcClassificationGQLModel"]:
        loader = getLoadersFromInfo(info).classifications
        result = await loader.filter_by(semester_id=self.id)
        return result

    @strawberry.field(
        description="""topics""")
    async def topics(self, info: strawberry.types.Info) -> typing.List["AcTopicGQLModel"]:
        loader = getLoadersFromInfo(info).topics
        result = await loader.filter_by(semester_id=self.id)
        return result
    
    @strawberry.field(
        description="""topics""")
    async def subject(self, info: strawberry.types.Info) -> typing.List["AcSubjectGQLModel"]:
        loader = getLoadersFromInfo(info).subjects
        result = await loader.filter_by(id=self.subject_id)
        return result


#################################################
# Query
#################################################

from dataclasses import dataclass 
from uoishelpers.resolvers import createInputs
@createInputs
@dataclass 
class SemesterWhereFilter:
    subject_id: uuid.UUID
    classificationtype_id: uuid.UUID
    order: int
    credits: int
    valid: bool

from ._GraphResolvers import asPage

@strawberry.field(
    description="""Finds a subject semester by its id""",
    permission_classes=[OnlyForAuthentized()])
async def acsemester_by_id(
        self, info: strawberry.types.Info, id: uuid.UUID
    ) -> typing.Optional[AcSemesterGQLModel]:
        result = await AcSemesterGQLModel.resolve_reference(info, id)
        return result

@strawberry.field(
    description="""Finds a subject semester by its id""",
    permission_classes=[OnlyForAuthentized()])
@asPage
async def acsemester_page(
        self, info: strawberry.types.Info, skip: int = 0, limit: int = 10,
        where: typing.Optional[SemesterWhereFilter] = None
    ) -> typing.List[AcSemesterGQLModel]:
        return getLoadersFromInfo(info).semesters

#################################################
# Mutation
#################################################

@strawberry.input
class SemesterInsertGQLModel:
    subject_id:uuid.UUID
    classificationtype_id: uuid.UUID
    order: typing.Optional[int] = 0
    credits: typing.Optional[int] = 0
    id: typing.Optional[uuid.UUID] = None
    valid: typing.Optional[bool] = True

@strawberry.input
class SemesterUpdateGQLModel:
    id: uuid.UUID
    lastchange: datetime.datetime
    valid: typing.Optional[bool] = None
    order: typing.Optional[int] = None
    credits: typing.Optional[int] = None
    classificationtype_id: typing.Optional[uuid.UUID] = None

@strawberry.type
class SemesterResultGQLModel:
    id: uuid.UUID = None
    msg: str = None

    @strawberry.field(description="""Result of semester operation""")
    async def semester(self, info: strawberry.types.Info) -> typing.Union[AcSemesterGQLModel, None]:
        result = await AcSemesterGQLModel.resolve_reference(info, self.id)
        return result

@strawberry.mutation(
    description="""Adds a new semester to study program""",
    permission_classes=[OnlyForAuthentized()])
async def semester_insert(self, info: strawberry.types.Info, semester: SemesterInsertGQLModel) -> SemesterResultGQLModel:
        loader = getLoadersFromInfo(info).semesters
        row = await loader.insert(semester)
        print("semester_insert", row.id, row.classificationtype_id)
        result = SemesterResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        return result

@strawberry.mutation(
    description="""Update the semester of study program""",
    permission_classes=[OnlyForAuthentized()])
async def semester_update(self, info: strawberry.types.Info, semester: SemesterUpdateGQLModel) -> SemesterResultGQLModel:
        loader = getLoadersFromInfo(info).semesters
        row = await loader.update(semester)
        result = SemesterResultGQLModel()
        result.msg = "ok"
        result.id = semester.id
        result.msg = "ok" if (row is not None) else "fail"
            
        return result