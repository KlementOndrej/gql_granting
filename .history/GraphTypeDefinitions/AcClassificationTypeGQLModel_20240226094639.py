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

@strawberry.federation.type(
    keys=["id"], 
    description="Classification at the end of semester"
)
class AcClassificationTypeGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        loader = getLoadersFromInfo(info).classificationtypes
        return loader

    id = resolve_id
    name = resolve_name
    name_en = resolve_name_en
    lastchange = resolve_lastchange
