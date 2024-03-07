import strawberry
import typing
import datetime
import uuid
import logging
import asyncio

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

UserGQLModel= typing.Annotated["UserGQLModel",strawberry.lazy(".externals")]
AcSubjectGQLModel = typing.Annotated["AcSubjectGQLModel",strawberry.lazy(".AcSubjectGQLModel")]
AcProgramTypeGQLModel = typing.Annotated["AcProgramTypeGQLModel",strawberry.lazy(".AcProgramTypeGQLModel")]
GroupGQLModel= typing.Annotated["GroupGQLModel",strawberry.lazy(".externals")]

@strawberry.federation.type(
    keys=["id"], 
    description="""Entity representing acredited study programs"""
)
class AcProgramGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        loader = getLoadersFromInfo(info).programs
        return loader

    id = resolve_id
    name = resolve_name
    name_en = resolve_name_en
    lastchange = resolve_lastchange

    @strawberry.field(description="""Bachelor, ...""")
    async def type(self, info: strawberry.types.Info) -> typing.Optional["AcProgramTypeGQLModel"]:
        from .AcProgramTypeGQLModel import AcProgramTypeGQLModel
        result = await AcProgramTypeGQLModel.resolve_reference(info, self.type_id)
        return result

    @strawberry.field(description="""subjects in the program""")
    async def subjects(self, info: strawberry.types.Info) -> typing.List["AcSubjectGQLModel"]:
        loader = getLoadersFromInfo(info).subjects
        result = await loader.filter_by(program_id=self.id)
        return result

    @strawberry.field(description="""students in the program""")
    async def students(self, info: strawberry.types.Info) -> typing.List["UserGQLModel"]:
        loader = getLoadersFromInfo(info).programstudents
        rows = await loader.filter_by(program_id=self.id)
        from .externals import UserGQLModel
        userawaitables = (UserGQLModel.resolve_reference(row.student_id) for row in rows)
        result = await asyncio.gather(*userawaitables)
        return result

    @strawberry.field(description="""group defining grants of this program""")
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
class ProgramWhereFilter:
    name: str 
    name_en:str 
    type_id : uuid.UUID

from ._GraphResolvers import asPage


@strawberry.field(
    description="""Finds an program by their id""",
    permission_classes=[OnlyForAuthentized()])
async def program_by_id(
        self, info: strawberry.types.Info, id: uuid.UUID
    ) -> typing.Optional[AcProgramGQLModel]:
        result = await AcProgramGQLModel.resolve_reference(info=info, id=id)
        return result

@strawberry.field(
    description="""Finds all programs""",
    permission_classes=[OnlyForAuthentized()])
@asPage
async def program_page( 
        self, info: strawberry.types.Info, skip: int = 0, limit: int = 10,
        where: typing.Optional[ProgramWhereFilter] = None
    ) -> typing.List[AcProgramGQLModel]:
        return getLoadersFromInfo(info).programs 
    
#################################################
# Mutation
#################################################

@strawberry.input(description="Define input for the program" )
class ProgramInsertGQLModel:
    name: str
    type_id: uuid.UUID
    id: typing.Optional[uuid.UUID] = None
    pass

@strawberry.input(description="Update type of the program")
class ProgramUpdateGQLModel:
    id: uuid.UUID
    lastchange: datetime.datetime
    name: typing.Optional[str] = None
    name_en: typing.Optional[str] = None
    type_id: typing.Optional[uuid.UUID] = None

@strawberry.type
class ProgramResultGQLModel:
    id: uuid.UUID = None
    msg: str = None

    @strawberry.field(description="""Result of user operation""")
    async def program(self, info: strawberry.types.Info) -> typing.Union[AcProgramGQLModel, None]:
        result = await AcProgramGQLModel.resolve_reference(info, self.id)
        return result


@strawberry.mutation(
    description="""Adds new study program""",
    permission_classes=[OnlyForAuthentized()])
async def program_insert(self, info: strawberry.types.Info, program: ProgramInsertGQLModel) -> ProgramResultGQLModel:
        loader = getLoadersFromInfo(info).programs
        row = await loader.insert(program)
        result = ProgramResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        return result

@strawberry.mutation(
    description="""Update the study program""",
    permission_classes=[OnlyForAuthentized()])
async def program_update(self, info: strawberry.types.Info, program: ProgramUpdateGQLModel) -> ProgramResultGQLModel:
        loader = getLoadersFromInfo(info).programs
        row = await loader.update(program)
        result = ProgramResultGQLModel()
        result.msg = "ok"
        result.id = program.id
        if row is None:
            result.msg = "fail"
            
        return result

    
