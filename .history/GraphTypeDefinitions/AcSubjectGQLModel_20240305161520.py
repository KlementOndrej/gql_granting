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

AcProgramGQLModel = typing.Annotated["AcProgramGQLModel",strawberry.lazy(".AcProgramGQLModel")]
AcSemesterGQLModel = typing.Annotated["AcSemesterGQLModel",strawberry.lazy(".AcSemesterGQLModel")]
GroupGQLModel= typing.Annotated["GroupGQLModel",strawberry.lazy(".externals")]

@strawberry.federation.type(
    keys=["id"],
    description="""Entity which connects programs and semesters, includes informations about subjects (divided into semesters)""",
)
class AcSubjectGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        loader = getLoadersFromInfo(info).subjects
        return loader

    id = resolve_id
    name = resolve_name
    name_en = resolve_name_en
    lastchange = resolve_lastchange

    @strawberry.field(
        description="""Program owing this subjects""")
    async def program(self, info: strawberry.types.Info) -> typing.Optional["AcProgramGQLModel"]:
        from .AcProgramGQLModel import AcProgramGQLModel
        result = await AcProgramGQLModel.resolve_reference(info, self.program_id)
        return result

    @strawberry.field(
        description="""Semesters which the subjects in divided into""")
    async def semesters(
        self, info: strawberry.types.Info
    ) -> typing.List["AcSemesterGQLModel"]:
        loader = getLoadersFromInfo(info).semesters
        result = await loader.filter_by(subject_id=self.id)
        return result

    @strawberry.field(
        description="""group defining grants of this subject""")
    async def grants(self, info: strawberry.types.Info) -> typing.Optional["GroupGQLModel"]:
        loader = getLoadersFromInfo(info).programgroups
        rows = await loader.filter_by(program_id=self.id)
        result = next(rows, None)
        return result

#################################################
# Query
#################################################

from dataclasses import dataclass 
from uoishelpers.resolvers import createInputs
@createInputs
@dataclass 
class SubjectWhereFilter:
    name: str
    name_en: str
    program_id: uuid.UUID
    valid: bool

from ._GraphResolvers import asPage

@strawberry.field(
    description="""Finds a subject by its id""",
    permission_classes=[OnlyForAuthentized()])
async def acsubject_by_id(
        self, info: strawberry.types.Info, id: uuid.UUID
    ) -> typing.Optional[AcSubjectGQLModel]:
        result = await AcSubjectGQLModel.resolve_reference(info, id)
        return result

@strawberry.field(
    description="""Find all subjects""",
    permission_classes=[OnlyForAuthentized()])
@asPage
async def acsubject_page(
        self, info: strawberry.types.Info, skip: int = 0, limit: int = 10, 
        where: typing.Optional[SubjectWhereFilter] = None
    ) -> typing.List[AcSubjectGQLModel]:
        return getLoadersFromInfo(info).subjects
    
#################################################
# Mutation
#################################################

@strawberry.input
class SubjectInsertGQLModel:
    name: str
    name_en: str
    program_id: uuid.UUID
    id: typing.Optional[uuid.UUID] = None
    valid: typing.Optional[bool] = True

@strawberry.input
class SubjectUpdateGQLModel:
    id: uuid.UUID
    lastchange: datetime.datetime
    name: typing.Optional[str] = None
    name_en: typing.Optional[str] = None
    valid: typing.Optional[bool] = None

@strawberry.type
class SubjectResultGQLModel:
    id: uuid.UUID = None
    msg: str = None

    @strawberry.field(description="""Result of subject operation""")
    async def subject(self, info: strawberry.types.Info) -> typing.Union[AcSubjectGQLModel, None]:
        result = await AcSubjectGQLModel.resolve_reference(info, self.id)
        return result
    
@strawberry.mutation(
    description="""Adds a new study subject""",
    permission_classes=[OnlyForAuthentized()])
async def subject_insert(self, info: strawberry.types.Info, subject: SubjectInsertGQLModel) -> SubjectResultGQLModel:
        loader = getLoadersFromInfo(info).subjects
        row = await loader.insert(subject)
        result = SubjectResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        return result

@strawberry.mutation(
    description="""Update the study subject""",
    permission_classes=[OnlyForAuthentized()])
async def subject_update(self, info: strawberry.types.Info, subject: SubjectUpdateGQLModel) -> SubjectResultGQLModel:
        loader = getLoadersFromInfo(info).subjects
        row = await loader.update(subject)
        result = SubjectResultGQLModel()
        result.msg = "ok"
        result.id = subject.id
        result.msg = "ok" if (row is not None) else "fail"
            
        return result