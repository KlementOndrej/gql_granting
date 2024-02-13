import strawberry
import datetime
import asyncio
from uuid import UUID 
from typing import Optional, List, Union, Annotated

from .externals import GroupGQLModel 

def getLoaders(info):
    return info.context['all']
def getUser(info):
    return info.context["user"]

AcProgramGQLModel = Annotated["AcProgramGQLModel",strawberry.lazy(".AcProgramGQLModel")]
AcSemesterGQLModel =Annotated["AcSemesterGQLModel",strawberry.lazy(".AcSemesterGQLModel")]

@strawberry.federation.type(
    keys=["id"],
    description="""Entity which connects programs and semesters, includes informations about subjects (divided into semesters)""",
)
class AcSubjectGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: UUID):
        loader = getLoaders(info).subjects
        result = await loader.load(id)
        if result is not None:
            result.__strawberry_definition__ = cls.__strawberry_definition__  # little hack :)
        return result

    @strawberry.field(description="""primary key""")
    def id(self) -> UUID:
        return self.id

    @strawberry.field(description="""time stamp""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberry.field(description="""name""")
    def name(self) -> str:
        return self.name

    @strawberry.field(description="""english name""")
    def name_en(self) -> str:
        return self.name_en

    @strawberry.field(description="""datetime laschange""")
    def lastchange(self) -> str:
        return self.lastchange

    @strawberry.field(description="""Program owing this subjects""")
    async def program(self, info: strawberry.types.Info) -> Optional["AcProgramGQLModel"]:
        from .AcProgramGQLModel import AcProgramGQLModel
        result = await AcProgramGQLModel.resolve_reference(info, self.program_id)
        return result

    @strawberry.field(description="""Semesters which the subjects in divided into""")
    async def semesters(
        self, info: strawberry.types.Info
    ) -> List["AcSemesterGQLModel"]:
        loader = getLoaders(info).semesters
        result = await loader.filter_by(subject_id=self.id)
        return result

    @strawberry.field(description="""group defining grants of this subject""")
    async def grants(self, info: strawberry.types.Info) -> Optional["GroupGQLModel"]:
        loader = getLoaders(info).programgroups
        rows = await loader.filter_by(program_id=self.id)
        result = next(rows, None)
        return result

#################################################
# Query
#################################################

@strawberry.field(description="""Finds a subject by its id""")
async def acsubject_by_id(
        self, info: strawberry.types.Info, id: UUID
    ) -> Optional[AcSubjectGQLModel]:
        result = await AcSubjectGQLModel.resolve_reference(info, id)
        return result

@strawberry.field(description="""Find all subjects""")
async def acsubject_page(
        self, info: strawberry.types.Info, skip: Optional[int] = 0, limit: Optional[int] = 10
    ) -> List["AcSubjectGQLModel"]:
        loader = getLoaders(info).subjects
        result = await loader.page()
        #result = await AcSubjectGQLModel.resolve_reference(info, id)
        return result
    
#################################################
# Mutation
#################################################

@strawberry.input
class SubjectInsertGQLModel:
    name: str
    name_en: str
    program_id: UUID
    id: Optional[UUID] = None
    valid: Optional[bool] = True

@strawberry.input
class SubjectUpdateGQLModel:
    id: UUID
    lastchange: datetime.datetime
    name: Optional[str] = None
    name_en: Optional[str] = None
    valid: Optional[bool] = None

@strawberry.type
class SubjectResultGQLModel:
    id: UUID = None
    msg: str = None

    @strawberry.field(description="""Result of subject operation""")
    async def subject(self, info: strawberry.types.Info) -> Union[AcSubjectGQLModel, None]:
        result = await AcSubjectGQLModel.resolve_reference(info, self.id)
        return result
    
@strawberry.mutation(description="""Adds a new study subject""")
async def subject_insert(self, info: strawberry.types.Info, subject: SubjectInsertGQLModel) -> SubjectResultGQLModel:
        loader = getLoaders(info).subjects
        row = await loader.insert(subject)
        result = SubjectResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        return result

@strawberry.mutation(description="""Update the study subject""")
async def subject_update(self, info: strawberry.types.Info, subject: SubjectUpdateGQLModel) -> SubjectResultGQLModel:
        loader = getLoaders(info).subjects
        row = await loader.update(subject)
        result = SubjectResultGQLModel()
        result.msg = "ok"
        result.id = subject.id
        if row is None:
            result.msg = "fail"
            
        return result