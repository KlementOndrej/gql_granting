from typing import List, Union
import typing
import strawberry
import uuid
from contextlib import asynccontextmanager



###########################################################################################################################
#
# zde definujte sve GQL modely
# - nove, kde mate zodpovednost
# - rozsirene, ktere existuji nekde jinde a vy jim pridavate dalsi atributy
#
###########################################################################################################################


# from gql_forms.GraphResolvers import resolveRequestsByThreeLetters



from .externals import UserGQLModel, GroupGQLModel
from ._GraphPermissions import RoleBasedPermission
from utils.Dataloaders import getUserFromInfo

###########################################################################################################################
# Query
###########################################################################################################################

@strawberry.type(description="""Type for query root""")
class Query:
    @strawberry.field(description="""Say hello to the world""")
    async def say_hello_forms(
        self, info: strawberry.types.Info, id: uuid.UUID
    ) -> Union[str, None]:
        user = getUserFromInfo(info)
        result = f"Hello {id} `{user}`"
        return result

    from .AcClassificationGQLModel import acclassification_by_id, acclassification_page
    acclassification_page = acclassification_page
    acclassification_by_id = acclassification_by_id

    from .AcSemesterGQLModel import acsemester_by_id, acsemester_page
    acsemester_by_id = acsemester_by_id
    acsemester_page = acsemester_page

    from .AcSubjectGQLModel import acsubject_by_id, acsubject_page
    acsubject_by_id = acsubject_by_id
    acsubject_page = acsubject_page

    from .AcTopicGQLModel import actopic_by_id, actopic_page
    actopic_by_id = actopic_by_id
    actopic_page = actopic_page

    from .AcLessonGQLModel import aclesson_by_id, aclesson_page
    aclesson_by_id = aclesson_by_id
    aclesson_page = aclesson_page
    
    from .AcProgramTypeGQLModel import program_type_by_id, program_type_page
    program_type_by_id = program_type_by_id
    program_type_page = program_type_page

    from .AcProgramGQLModel import program_by_id, program_page
    program_by_id = program_by_id
    program_page = program_page

###########################################################################################################################
# Mutation
###########################################################################################################################

   
@strawberry.type(description="""Type for mutation root""")
class Mutation:
    from .AcClassificationGQLModel import classification_insert
    classification_insert = classification_insert

    from .AcClassificationGQLModel import classification_update 
    classification_update= classification_update 

    from .AcSemesterGQLModel import semester_insert, semester_update
    semester_insert = semester_insert
    semester_update = semester_update

    from .AcSubjectGQLModel import subject_insert, subject_update
    subject_insert = subject_insert
    subject_update = subject_update

    from .AcTopicGQLModel import topic_insert, topic_update
    topic_insert = topic_insert
    topic_update = topic_update

    from .AcLessonGQLModel import lesson_insert, lesson_update
    lesson_insert = lesson_insert
    lesson_update = lesson_update

    from .AcProgramTypeGQLModel import program_type_insert, program_type_update
    program_type_insert = program_type_insert
    program_type_update = program_type_update
    
    from .AcProgramGQLModel import program_insert, program_update
    program_insert = program_insert
    program_update = program_update

###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

schema = strawberry.federation.Schema(Query, types=(UserGQLModel, GroupGQLModel), mutation=Mutation)
