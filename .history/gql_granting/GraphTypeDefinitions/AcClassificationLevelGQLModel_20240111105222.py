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
    keys=["id"],
    description="""Mark which student could get as an exam evaluation""",
)
class AcClassificationLevelGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: UUID):
        loader = getLoaders(info).classificationlevels
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
    
