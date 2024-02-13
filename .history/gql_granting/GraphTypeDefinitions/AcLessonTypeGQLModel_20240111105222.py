import strawberry
import datetime
import asyncio
from uuid import UUID 
from typing import Optional, List, Union, Annotated

def getLoaders(info):
    return info.context['all']
def getUser(info):
    return info.context["user"]

@strawberry.federation.type(keys=["id"], description="P, C, LC, S, ...")
class AcLessonTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: UUID):
        loader = getLoaders(info).lessontypes
        result = await loader.load(id)
        if result is not None:
            result.__strawberry_definition__ = cls.__strawberry_definition__  # little hack :)
        return result

    @strawberry.field(description="primary key")
    def id(self) -> UUID:
        return self.id

    @strawberry.field(description="name")
    def name(self) -> str:
        return self.name

    @strawberry.field(description="english name")
    def name_en(self) -> str:
        return self.name_en

    @strawberry.field(description="datetime lastchange")
    def lastchange(self) -> str:
        return self.lastchange
    
#################################################
# Query
#################################################

@strawberry.field(description="""Finds a lesson type by its id""")
async def aclesson_type_by_id(
        self, info: strawberry.types.Info, id: UUID
    ) -> Union["AcLessonTypeGQLModel", None]:
        result = await AcLessonTypeGQLModel.resolve_reference(info, id)
        return result
@strawberry.field(description="""Gets all lesson types""")
async def aclesson_type_page(
        self, info: strawberry.types.Info
    ) -> List["AcLessonTypeGQLModel"]:
        loader = getLoaders(info).lessontypes
        rows = await loader.execute_select(loader.getSelectStatement())
        return rows

