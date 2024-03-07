import strawberry
import typing
import datetime
import uuid
import logging

from utils.Dataloaders import getLoadersFromInfo, getUserFromInfo
from .BaseGQLModel import BaseGQLModel


from GraphTypeDefinitions._GraphResolvers import (
    resolve_id,
    resolve_name,
    resolve_name_en,
    resolve_changedby,
    resolve_created,
    resolve_lastchange,
    resolve_createdby,
    resolve_rbacobject,
    createRootResolver_by_id,
)
from ._GraphPermissions import RoleBasedPermission, OnlyForAuthentized

UserGQLModel= typing.Annotated["UserGQLModel",strawberry.lazy(".externals")]
AcSemesterGQLModel= typing.Annotated["AcSemesterGQLModel",strawberry.lazy(".AcSemesterGQLModel")]
AcClassificationTypeGQLModel= typing.Annotated["AcClassificationTypeGQLModel",strawberry.lazy(".AcClassificationTypeGQLModel")]
AcClassificationLevelGQLModel = typing.Annotated["AcClassificationLevelGQLModel",strawberry.lazy(".AcClassificationLevelGQLModel")]

@strawberry.federation.type(
    keys=["id"],
    description="""Entity which holds a exam result for a subject semester and user / student""",
)
class AcClassificationGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        loader = getLoadersFromInfo(info).classifications
        return loader

    id = resolve_id
    lastchange = resolve_lastchange

    @strawberry.field(
        description="""datetime of classification""")
    def date(self) -> datetime.datetime:
        return self.date

    @strawberry.field(
        description="""order of classification""")
    def order(self) -> int:
        return self.order

    @strawberry.field(
        description="""User""")
    async def user(self, info: strawberry.types.Info) -> typing.Optional["UserGQLModel"]:
        from .externals import UserGQLModel
        return await UserGQLModel.resolve_reference(info, id=self.user_id)

    @strawberry.field(
        description="""Semester""")
    async def semester(self, info: strawberry.types.Info) -> typing.Optional["AcSemesterGQLModel"]:
        from .AcSemesterGQLModel import AcSemesterGQLModel
        result = await AcSemesterGQLModel.resolve_reference(info, id=self.semester_id)
        return result
        
    @strawberry.field(
        description="""Level""")
    async def level(self, info: strawberry.types.Info) -> typing.Optional["AcClassificationLevelGQLModel"]:
        from .AcClassificationLevelGQLModel import AcClassificationLevelGQLModel
        result = await AcClassificationLevelGQLModel.resolve_reference(info, id=self.classificationlevel_id)
        return result

#################################################
# Query
#################################################

from dataclasses import dataclass 
from uoishelpers.resolvers import createInputs 
@createInputs 
@dataclass 
class ClassificationWhereFilter: 
    semester_id: uuid.UUID
    user_id: uuid.UUID
    classificationlevel_id: uuid.UUID
    order: int

from ._GraphResolvers import asPage

@strawberry.field(
    description="""Finds a classification by its id""",
    permission_classes=[OnlyForAuthentized()])
async def acclassification_by_id(
        self, info: strawberry.types.Info, id: uuid.UUID
    ) -> typing.Optional[AcClassificationGQLModel]:
        result = await AcClassificationGQLModel.resolve_reference(info, id)
        return result

@strawberry.field(
    description="""Lists classifications""",
    permission_classes=[OnlyForAuthentized()])
@asPage
async def acclassification_page(
        self, info: strawberry.types.Info, skip: int = 0, limit: int = 10,
        where: typing.Optional[ClassificationWhereFilter] = None
    ) -> typing.List[AcClassificationGQLModel]:
        return getLoadersFromInfo(info).classifications
    
#################################################
# Mutation
#################################################

@strawberry.input
class ClassificationInsertGQLModel:
    semester_id: uuid.UUID
    user_id: uuid.UUID
    classificationlevel_id: uuid.UUID
    order: int
    id: typing.Optional[uuid.UUID] = None

@strawberry.input
class ClassificationUpdateGQLModel:
    id: uuid.UUID
    lastchange: datetime.datetime
    classificationlevel_id: uuid.UUID

@strawberry.type
class ClassificationResultGQLModel:
    id: uuid.UUID = None
    msg: str = None

    @strawberry.field(description="""Result of semester operation""")
    async def classification(self, info: strawberry.types.Info) -> typing.Union[AcClassificationGQLModel, None]:
        result = await AcClassificationGQLModel.resolve_reference(info, self.id)
        return result
    
@strawberry.mutation(
    description="""Adds new classification (a mark for student)""",
    permission_classes=[OnlyForAuthentized()])
async def classification_insert(self, info: strawberry.types.Info, classification: ClassificationInsertGQLModel) -> ClassificationResultGQLModel:
    print("classification_insert", classification)
    loader = getLoadersFromInfo(info).classifications
    row = await loader.insert(classification)
    result = ClassificationResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result

@strawberry.mutation(
    description="""Update the classification (a mark for student)""",
    permission_classes=[OnlyForAuthentized()])
async def classification_update(self, info: strawberry.types.Info, classification: ClassificationUpdateGQLModel) -> ClassificationResultGQLModel:
        loader = getLoadersFromInfo(info).classifications
        row = await loader.update(classification)
        result = ClassificationResultGQLModel()
        result.msg = "ok"
        result.id = classification.id
        result.msg = "ok" if (row is not None) else "fail"
            
        return result
