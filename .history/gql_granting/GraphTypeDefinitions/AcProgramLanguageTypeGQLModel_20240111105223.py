import strawberry
import datetime
import asyncio
from uuid import UUID 
from typing import Optional, List, Union, Annotated

from gql_granting.utils.GraphResolvers import resolveLanguageTypeById

def getLoaders(info):
    return info.context['all']
def getUser(info):
    return info.context["user"]

@strawberry.federation.type(keys=["id"], description="Study program language")
class AcProgramLanguageTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: UUID):
        loader = getLoaders(info).programlanguages
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberry.field(description="primary key")
    def id(self) -> UUID:
        return self.id

    @strawberry.field(description="name (like čeština)")
    def name(self) -> str:
        return self.name

    @strawberry.field(description="name (like Czech)")
    def name_en(self) -> str:
        return self.name_en

    @strawberry.field(description="")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange
    
#################################################
# Query
#################################################

@strawberry.field(description="""Finds a program language its id""")
async def program_language_by_id(
        self, info: strawberry.types.Info, id:UUID
    ) -> Union["AcProgramLanguageTypeGQLModel", None]:
        result = await AcProgramLanguageTypeGQLModel.resolve_reference(info, id)
        return result

