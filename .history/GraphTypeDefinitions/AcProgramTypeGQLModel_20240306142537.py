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

AcProgramFormTypeGQLModel = typing.Annotated["AcProgramFormTypeGQLModel",strawberry.lazy(".AcProgramFormTypeGQLModel")]
AcProgramTitleTypeGQLModel = typing.Annotated["AcProgramTitleTypeGQLModel",strawberry.lazy(".AcProgramTitleTypeGQLModel")]
AcProgramLevelTypeGQLModel = typing.Annotated["AcProgramLevelTypeGQLModel",strawberry.lazy(".AcProgramLevelTypeGQLModel")]
AcProgramLanguageTypeGQLModel = typing.Annotated["AcProgramLanguageTypeGQLModel",strawberry.lazy(".AcProgramLanguageTypeGQLModel")]

@strawberry.federation.type(
    keys=["id"],
    description="""Encapsulation of language, level, type etc. of program. This is intermediate entity for acredited program and its types""",
)
class AcProgramTypeGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        loader = getLoadersFromInfo(info).programtypes
        return loader
    
    id = resolve_id
    name = resolve_name
    name_en = resolve_name_en
    lastchange = resolve_lastchange

    @strawberry.field(description="""Bachelor, ...""")
    async def level(self, info: strawberry.types.Info) -> typing.Optional["AcProgramLevelTypeGQLModel"]:
        from .AcProgramLevelTypeGQLModel import AcProgramLevelTypeGQLModel
        result = await AcProgramLevelTypeGQLModel.resolve_reference(info, self.level_id)
        return result

    @strawberry.field(description="""Present, Distant, ...""")
    async def form(self, info: strawberry.types.Info) -> typing.Optional["AcProgramFormTypeGQLModel"]:
        from .AcProgramFormTypeGQLModel import AcProgramFormTypeGQLModel
        result = await AcProgramFormTypeGQLModel.resolve_reference(info, self.form_id)
        return result

    @strawberry.field(description="""Czech, ...""")
    async def language(
        self, info: strawberry.types.Info) -> typing.Optional["AcProgramLanguageTypeGQLModel"]:
        from .AcProgramLanguageTypeGQLModel import AcProgramLanguageTypeGQLModel
        result = await AcProgramLanguageTypeGQLModel.resolve_reference(info, self.language_id)
        return result

    @strawberry.field(
        description="""topics""")
    async def subject(self, info: strawberry.types.Info) -> typing.List["AcProgramTitleTypeGQLModel"]:
        loader = getLoadersFromInfo(info).programtitletypes
        result = await loader.filter_by(id=self.title_id)
        return result

#################################################
# Query
#################################################

from dataclasses import dataclass 
from uoishelpers.resolvers import createInputs
@createInputs
@dataclass 
class ProgramTypeWhereFilter:
    name: str 
    name_en:str 
    language_id: uuid.UUID
    level_id: uuid.UUID
    form_id: uuid.UUID
    title_id: uuid.UUID

from ._GraphResolvers import asPage

@strawberry.field(
    description="""Finds a program type its id""",
    permission_classes=[OnlyForAuthentized()])
async def program_type_by_id(
        self, info: strawberry.types.Info, id: uuid.UUID
    ) -> typing.Optional[AcProgramTypeGQLModel]:
        result = await AcProgramTypeGQLModel.resolve_reference(info, id)
        return result

@strawberry.field(
    description="""Finds all program types""",
    permission_classes=[OnlyForAuthentized()])
@asPage
async def program_page( 
        self, info: strawberry.types.Info, skip: int = 0, limit: int = 10,
        where: typing.Optional[ProgramTypeWhereFilter] = None
    ) -> typing.List[AcProgramTypeGQLModel]:
        return getLoadersFromInfo(info).programtypes

#################################################
# Mutation
#################################################

@strawberry.input
class ProgramTypeInsertGQLModel:
    name: str
    name_en: str
    language_id: uuid.UUID
    level_id: uuid.UUID
    form_id: uuid.UUID
    title_id: uuid.UUID
    id: typing.Optional[uuid.UUID] = None

@strawberry.input
class ProgramTypeUpdateGQLModel:
    id: uuid.UUID
    lastchange: datetime.datetime
    name: typing.Optional[str] = None
    name_en: typing.Optional[str] = None
    language_id: typing.Optional[uuid.UUID] = None
    level_id: typing.Optional[uuid.UUID] = None
    form_id: typing.Optional[uuid.UUID] = None
    title_id: typing.Optional[uuid.UUID] = None

@strawberry.type
class ProgramTypeResultGQLModel:
    id: uuid.UUID = None
    msg: str = None

    @strawberry.field(
        description="""Result of user operation""")
    async def program_type(self, info: strawberry.types.Info) -> typing.Union[AcProgramTypeGQLModel, None]:
        result = await AcProgramTypeGQLModel.resolve_reference(info, self.id)
        return result

@strawberry.mutation(
    description="""Adds a new study program type""",
    permission_classes=[OnlyForAuthentized()])
async def program_type_insert(self, info: strawberry.types.Info, program_type: ProgramTypeInsertGQLModel) -> ProgramTypeResultGQLModel:
        loader = getLoadersFromInfo(info).programtypes
        row = await loader.insert(program_type)
        result = ProgramTypeResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        return result
    
@strawberry.mutation(
    description="""Update the study program type""",
    permission_classes=[OnlyForAuthentized()])
async def program_type_update(self, info: strawberry.types.Info, program_type: ProgramTypeUpdateGQLModel) -> ProgramTypeResultGQLModel:
        loader = getLoadersFromInfo(info).programtypes
        row = await loader.update(program_type)
        result = ProgramTypeResultGQLModel()
        result.msg = "ok"
        result.id = program_type.id
        result.msg = "ok" if (row is not None) else "fail"
        return result
    