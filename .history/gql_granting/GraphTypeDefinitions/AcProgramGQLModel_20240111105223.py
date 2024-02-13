import strawberry
import datetime
import asyncio
from uuid import UUID 
from typing import Optional, List, Union, Annotated

from .AcProgramEditorGQLModel import AcProgramEditorGQLModel

def getLoaders(info):
    return info.context['all']
def getUser(info):
    return info.context["user"]

UserGQLModel= Annotated["UserGQLModel",strawberry.lazy(".externals")]
AcSubjectGQLModel = Annotated["AcSubjectGQLModel",strawberry.lazy(".AcSubjectGQLModel")]
AcProgramTypeGQLModel = Annotated["AcProgramTypeGQLModel",strawberry.lazy(".AcProgramTypeGQLModel")]
GroupGQLModel= Annotated["GroupGQLModel",strawberry.lazy(".externals")]

@strawberry.federation.type(
    keys=["id"], description="""Entity representing acredited study programs"""
)
class AcProgramGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: UUID):
        if isinstance(id, str):
             id = UUID(id)
        loader = getLoaders(info).programs
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

    @strawberry.field(description="""name""")
    def name_en(self) -> str:
        return self.name_en

    @strawberry.field(description="""""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberry.field(description="""Bachelor, ...""")
    async def type(self, info: strawberry.types.Info) -> Optional["AcProgramTypeGQLModel"]:
        from .AcProgramTypeGQLModel import AcProgramTypeGQLModel
        result = await AcProgramTypeGQLModel.resolve_reference(info, self.type_id)
        return result

    @strawberry.field(description="""""")
    def editor(self) -> "AcProgramEditorGQLModel":
        return self

    @strawberry.field(description="""subjects in the program""")
    async def subjects(self, info: strawberry.types.Info) -> List["AcSubjectGQLModel"]:
        loader = getLoaders(info).subjects
        result = await loader.filter_by(program_id=self.id)
        return result

    @strawberry.field(description="""students in the program""")
    async def students(self, info: strawberry.types.Info) -> List["UserGQLModel"]:
        loader = getLoaders(info).programstudents
        rows = await loader.filter_by(program_id=self.id)
        from .externals import UserGQLModel
        userawaitables = (UserGQLModel.resolve_reference(row.student_id) for row in rows)
        result = await asyncio.gather(*userawaitables)
        return result

    @strawberry.field(description="""group defining grants of this program""")
    async def grants(self, info: strawberry.types.Info) -> Optional["GroupGQLModel"]:
        loader = getLoaders(info).programgroups
        rows = await loader.filter_by(program_id=self.id)
        result = next(rows, None)
        return result

#################################################
# Query
#################################################

from typing import Any, NewType

JSON = strawberry.scalar(
    NewType("JSON", object),
    description="The `JSON` scalar type represents JSON values as specified by ECMA-404",
    serialize=lambda v: v,
    parse_value=lambda v: v,
)
class ProgramWhereFilter:
    name: str 
    name_en:str 
    

@strawberry.field(description="""Finds an program by their id""")
async def program_by_id(
        self, info: strawberry.types.Info, id: UUID #strawberry.ID
    ) -> Optional[AcProgramGQLModel]:
        print(type(id))
        result = await AcProgramGQLModel.resolve_reference(info=info, id=id)
        return result

@strawberry.field(description="""Finds all programs""")
async def program_page( 
        self, info: strawberry.types.Info, skip: int = 0, limit: int = 10
    ) -> List["AcProgramGQLModel"]:
        loader = getLoaders(info).programs 
        result = await loader.page(skip=skip, limit=limit)
        return result
    
#################################################
# Mutation
#################################################

@strawberry.input(description="Define input for the program" )
class ProgramInsertGQLModel:
    name: str
    type_id: UUID
    id: Optional[UUID] = None
    pass

@strawberry.input(description="Update type of the program")
class ProgramUpdateGQLModel:
    id: UUID
    lastchange: datetime.datetime
    name: Optional[str] = None
    name_en: Optional[str] = None
    type_id: Optional[UUID] = None

@strawberry.type
class ProgramResultGQLModel:
    id: UUID = None
    msg: str = None

    @strawberry.field(description="""Result of user operation""")
    async def program(self, info: strawberry.types.Info) -> Union[AcProgramGQLModel, None]:
        result = await AcProgramGQLModel.resolve_reference(info, self.id)
        return result


@strawberry.mutation(description="""Adds new study program""")
async def program_insert(self, info: strawberry.types.Info, program: ProgramInsertGQLModel) -> ProgramResultGQLModel:
        loader = getLoaders(info).programs
        row = await loader.insert(program)
        result = ProgramResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        return result

@strawberry.mutation(description="""Update the study program""")
async def program_update(self, info: strawberry.types.Info, program: ProgramUpdateGQLModel) -> ProgramResultGQLModel:
        loader = getLoaders(info).programs
        row = await loader.update(program)
        result = ProgramResultGQLModel()
        result.msg = "ok"
        result.id = program.id
        if row is None:
            result.msg = "fail"
            
        return result

    
