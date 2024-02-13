import strawberry
import datetime
import asyncio
from uuid import UUID 
from typing import Optional, List, Union, Annotated

def getLoaders(info):
    return info.context['all']
def getUser(info):
    return info.context["user"]

@strawberry.federation.type(keys=["id"], description="Bc., Ing., ...")
class AcProgramTitleTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: UUID):
        loader = getLoaders(info).programtitletypes
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

@strawberry.field(description="""Finds a program title by its id""")
async def program_title_by_id(
        self, info: strawberry.types.Info, id: UUID
    ) -> Union["AcProgramTitleTypeGQLModel", None]:
        result = await AcProgramTitleTypeGQLModel.resolve_reference(info, id)
        return result


