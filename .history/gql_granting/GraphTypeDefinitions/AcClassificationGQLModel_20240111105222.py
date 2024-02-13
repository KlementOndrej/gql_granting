import strawberry
import datetime
import asyncio
from uuid import UUID 
from typing import Optional, List, Union, Annotated

from .AcClassificationLevelGQLModel import AcClassificationLevelGQLModel


def getLoaders(info):
    return info.context['all']
def getUser(info):
    return info.context["user"]

UserGQLModel= Annotated["UserGQLModel",strawberry.lazy(".externals")]
AcSemesterGQLModel= Annotated["AcSemesterGQLModel",strawberry.lazy(".AcSemesterGQLModel")]

@strawberry.federation.type(
    keys=["id"],
    description="""Entity which holds a exam result for a subject semester and user / student""",
)
class AcClassificationGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: UUID):
        print("AcClassificationGQLModel.resolve_reference", type(id))
        if not isinstance(id, UUID):
            id = UUID(id)
            
        loader = getLoaders(info).classifications
        # print("AcClassificationGQLModel.resolve_reference", loader)
        result = await loader.load(id)
        print(result)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
            result.__strawberry_definition__ = cls.__strawberry_definition__
        return result

    @strawberry.field(description="""primary key""")
    def id(self) -> UUID:
        return self.id

    @strawberry.field(description="""datetime lastchange""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberry.field(description="""datetime of classification""")
    def date(self) -> datetime.datetime:
        return self.date

    @strawberry.field(description="""order of classification""")
    def order(self) -> int:
        return self.order

    @strawberry.field(description="""User""")
    async def user(self, info: strawberry.types.Info) -> Optional["UserGQLModel"]:
        from .externals import UserGQLModel
        return await UserGQLModel.resolve_reference(id=self.user_id)

    @strawberry.field(description="""Semester""")
    async def semester(self, info: strawberry.types.Info) -> Optional["AcSemesterGQLModel"]:
        from .AcSemesterGQLModel import AcSemesterGQLModel
        result = await AcSemesterGQLModel.resolve_reference(info, id=self.semester_id)
        return result

    # @strawberry.field(description="""Type""")
    # async def type(self, info: strawberry.types.Info) -> "AcClassificationTypeGQLModel":
    #     result = await AcClassificationTypeGQLModel.resolve_reference(info, id=self.classificationtype_id)
    #     return result

    @strawberry.field(description="""Level""")
    async def level(self, info: strawberry.types.Info) -> "AcClassificationLevelGQLModel":
        result = await AcClassificationLevelGQLModel.resolve_reference(info, id=self.classificationlevel_id)
        return result

#################################################
# Query
#################################################

@strawberry.field(description="""Lists classifications""")
async def acclassification_page(
        self, info: strawberry.types.Info, skip: int = 0, limit: int = 10
    ) -> List["AcClassificationGQLModel"]:
        loader = getLoaders(info).classifications
        result = await loader.page(skip=skip, limit=limit)
        return result

@strawberry.field(description="""Lists classifications for the user""")
async def acclassification_page_by_user(
        self, info: strawberry.types.Info, user_id: UUID, skip: int = 0, limit: int = 10
    ) -> List["AcClassificationGQLModel"]:
        loader = getLoaders(info).classifications
        result = await loader.filter_by(user_id=user_id)
        return result

#################################################
# Mutation
#################################################

@strawberry.input
class ClassificationInsertGQLModel:
    semester_id: UUID
    user_id: UUID
    classificationlevel_id: UUID
    order: int
    id: Optional[UUID] = None

@strawberry.input
class ClassificationUpdateGQLModel:
    id: UUID
    lastchange: datetime.datetime
    classificationlevel_id: UUID

@strawberry.type
class ClassificationResultGQLModel:
    id: UUID = None
    msg: str = None

    @strawberry.field(description="""Result of semester operation""")
    async def classification(self, info: strawberry.types.Info) -> Union[AcClassificationGQLModel, None]:
        result = await AcClassificationGQLModel.resolve_reference(info, self.id)
        return result
    
@strawberry.mutation(description="""Adds new classification (a mark for student)""")
async def classification_insert(self, info: strawberry.types.Info, classification: ClassificationInsertGQLModel) -> ClassificationResultGQLModel:
    print("classification_insert", classification)
    loader = getLoaders(info).classifications
    row = await loader.insert(classification)
    result = ClassificationResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result

@strawberry.mutation(description="""Update the classification (a mark for student)""")
async def classification_update(self, info: strawberry.types.Info, classification: ClassificationUpdateGQLModel) -> ClassificationResultGQLModel:
        loader = getLoaders(info).classifications
        row = await loader.update(classification)
        result = ClassificationResultGQLModel()
        result.msg = "ok"
        result.id = classification.id
        if row is None:
            result.msg = "fail"
            
        return result
