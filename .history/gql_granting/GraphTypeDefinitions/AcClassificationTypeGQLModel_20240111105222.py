import strawberry
import datetime
import asyncio
from uuid import UUID 
from typing import Optional, List, Union, Annotated

def getLoaders(info):
    return info.context['all']
def getUser(info):
    return info.context["user"]

#UserGQLModel= Annotated["UserGQLModel",strawberry.lazy(".granting")]

@strawberry.federation.type(
    keys=["id"], description="Classification at the end of semester"
)
class AcClassificationTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: UUID):
        loader = getLoaders(info).classificationtypes
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

@strawberry.field(description="""Lists classifications types""")
async def acclassification_type_page(
        self, info: strawberry.types.Info, user_id: UUID, skip: int = 0, limit: int = 10
    ) -> List["AcClassificationTypeGQLModel"]:
        loader = getLoaders(info).classificationtypes
        result = await loader.page(skip, limit)
        return result

