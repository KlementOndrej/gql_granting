import pytest
from GraphTypeDefinitions import schema
import datetime
# from ..shared import (
#     prepare_demodata,
#     prepare_in_memory_sqllite,
#     get_demodata,
#     createContext,
# )
from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)
test_reference_program_languages = createResolveReferenceTest(tableName='acprogramlanguages', gqltype='AcProgramLanguageTypeGQLModel', attributeNames=["id"])
test_query_program_language_by_id = createByIdTest(tableName="acprogramlanguages", queryEndpoint="programLanguageById",attributeNames=["id"])
