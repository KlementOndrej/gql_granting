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
  
)
from ._GraphPermissions import RoleBasedPermission, OnlyForAuthentized

@strawberry.federation.type(
    keys=["id"],
    description="""Mark which student could get as an exam evaluation""",
)
class AcClassificationLevelGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        loader = getLoadersFromInfo(info).classificationlevels
        return loader
    
    id = resolve_id
    name = resolve_name
    name_en = resolve_name_en
    ordervalue = resolver_ordervalue
