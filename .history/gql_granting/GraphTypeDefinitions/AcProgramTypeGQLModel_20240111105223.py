import strawberry
import datetime
import asyncio
from uuid import UUID 
from typing import Optional, List, Union, Annotated

from .AcProgramFormTypeGQLModel import AcProgramFormTypeGQLModel
from .AcProgramTitleTypeGQLModel import AcProgramTitleTypeGQLModel
from .AcProgramLevelTypeGQLModel import AcProgramLevelTypeGQLModel
from .AcProgramLanguageTypeGQLModel import AcProgramLanguageTypeGQLModel 

def getLoaders(info):    
    return info.context['all']
def getUser(info):
    return info.context["user"]

ProgramUpdateGQLModel= Annotated["ProgramUpdateGQLModel",strawberry.lazy(".AcProgramGQLModel")]

@strawberry.federation.type(
    keys=["id"],
    description="""Encapsulation of language, level, type etc. of program. This is intermediate entity for acredited program and its types""",
)
class AcProgramTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: UUID):
        loader = getLoaders(info).programtypes
        result = await loader.load(id)
        if result is not None:
            result.__strawberry_definition__ = cls.__strawberry_definition__  # little hack :)
        return result

    @strawberry.field(description="""primary key""")
    def id(self) -> UUID:
        return self.id

    @strawberry.field(description="""name""")
    def name(self) -> str:
        return self.name

    @strawberry.field(description="""english name""")
    def name_en(self) -> str:
        return self.name_en

    @strawberry.field(description="""datetime lastchange""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberry.field(description="""Bachelor, ...""")
    async def level(self, info: strawberry.types.Info) -> "AcProgramLevelTypeGQLModel":
        result = await AcProgramLevelTypeGQLModel.resolve_reference(info, self.level_id)
        return result

    @strawberry.field(description="""Present, Distant, ...""")
    async def form(self, info: strawberry.types.Info) -> "AcProgramFormTypeGQLModel":
        result = await AcProgramFormTypeGQLModel.resolve_reference(info, self.form_id)
        return result

    @strawberry.field(description="""Czech, ...""")
    async def language(
        self, info: strawberry.types.Info
    ) -> "AcProgramLanguageTypeGQLModel":
        result = await AcProgramLanguageTypeGQLModel.resolve_reference(info, self.language_id)
        return result

    @strawberry.field(description="""Bc., Ing., ...""")
    async def title(self, info: strawberry.types.Info) -> "AcProgramTitleTypeGQLModel":
        result = await AcProgramTitleTypeGQLModel.resolve_reference(info, self.title_id)
        return result

#################################################
# Query
#################################################

@strawberry.field(description="""Finds a program type its id""")
async def program_type_by_id(
        self, info: strawberry.types.Info, id: UUID
    ) -> Union["AcProgramTypeGQLModel", None]:
        result = await AcProgramTypeGQLModel.resolve_reference(info, id)
        return result

#################################################
# Mutation
#################################################

@strawberry.type
@strawberry.input
class ProgramTypeInsertGQLModel:
    name: str
    name_en: str
    language_id: UUID
    level_id: UUID
    form_id: UUID
    title_id: UUID
    id: Optional[UUID] = None

@strawberry.input
class ProgramTypeUpdateGQLModel:
    id: UUID
    lastchange: datetime.datetime
    name: Optional[str] = None
    name_en: Optional[str] = None
    language_id: Optional[UUID] = None
    level_id: Optional[UUID] = None
    form_id: Optional[UUID] = None
    title_id: Optional[UUID] = None

class ProgramTypeResultGQLModel:
    id: UUID = None
    msg: str = None

    @strawberry.field(description="""Result of user operation""")
    async def program_type(self, info: strawberry.types.Info) -> Union[AcProgramTypeGQLModel, None]:
        result = await AcProgramTypeGQLModel.resolve_reference(info, self.id)
        return result

@strawberry.mutation(description="""Adds a new study program type""")
async def program_type_insert(self, info: strawberry.types.Info, program_type: ProgramTypeInsertGQLModel) -> ProgramTypeResultGQLModel:
        loader = getLoaders(info).programtypes
        row = await loader.insert(program_type)
        result = ProgramTypeResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        return result
    
@strawberry.mutation(description="""Update the study program type""")
async def program_type_update(self, info: strawberry.types.Info, program_type: ProgramUpdateGQLModel) -> ProgramTypeResultGQLModel:
        loader = getLoaders(info).programtypes
        row = await loader.update(program_type)
        result = ProgramTypeResultGQLModel()
        result.msg = "ok"
        result.id = program_type.id
        if row is None:
            result.msg = "fail"
             
        return result
    