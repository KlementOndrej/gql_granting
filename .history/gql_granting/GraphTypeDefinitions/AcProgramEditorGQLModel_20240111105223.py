import strawberry
import datetime
import asyncio
from uuid import UUID 
from typing import Optional, List, Union, Annotated

def getLoaders(info):
    return info.context['all']
def getUser(info):
    return info.context["user"]

@strawberry.federation.type(keys=["id"], description="Study program editor")
class AcProgramEditorGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: UUID):
        loader = getLoaders(info).programs
        result = await loader.load(id)
        if result is not None:
            result.__strawberry_definition__ = cls.__strawberry_definition__  # little hack :)
        return result

    @strawberry.field(description="primary key")
    def id(self) -> UUID:
        return self.id

    # change name, add subject, delete subject

    # @strawberry.field(description="groups linked the program")
    # async def groups(self, info: strawberry.types.Info) -> List["GroupGQLModel"]:
    #     async with withInfo(info) as session:
    #         links = await resolveGroupIdsForProgram(session, self.id)
    #         result = list(map(lambda item: GroupGQLModel(id=item), links))
    #         return result


