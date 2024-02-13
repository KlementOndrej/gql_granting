import strawberry

@strawberry.type(description="""Type for query root""")
class Query:
    from .AcLessonGQLModel import aclesson_by_id
    aclesson_by_id = aclesson_by_id

    from .AcLessonGQLModel import aclesson_type_page
    aclesson_type_page = aclesson_type_page

    from .AcClassificationGQLModel import acclassification_page
    acclassification_page = acclassification_page

    from .AcClassificationGQLModel import acclassification_page_by_user
    acclassification_page_by_user = acclassification_page_by_user

    from .AcProgramGQLModel import program_by_id
    program_by_id = program_by_id

    from .AcProgramGQLModel import program_page 
    program_page = program_page 

    from .AcProgramTypeGQLModel import program_type_by_id
    program_type_by_id = program_type_by_id

    from .AcSemesterGQLModel import acsemester_page
    acsemester_page = acsemester_page 

    from .AcSubjectGQLModel import acsubject_by_id
    acsubject_by_id = acsubject_by_id 

    from .AcSubjectGQLModel import acsubject_page
    acsubject_page = acsubject_page

    from .AcTopicGQLModel import actopic_by_id 
    actopic_by_id = actopic_by_id
    
    from .AcProgramLanguageTypeGQLModel import program_language_by_id
    program_language_by_id = program_language_by_id

    from .AcProgramLevelTypeGQLModel import program_level_by_id
    program_level_by_id = program_language_by_id

    from .AcProgramFormTypeGQLModel import program_form_by_id
    program_form_by_id = program_form_by_id

    from .AcProgramTitleTypeGQLModel import program_title_by_id
    program_title_by_id = program_title_by_id

    from .AcSemesterGQLModel import acsemester_by_id
    acsemester_by_id = acsemester_by_id

    from .AcLessonTypeGQLModel import aclesson_type_by_id
    aclesson_type_by_id = aclesson_type_by_id

    from .AcClassificationTypeGQLModel import acclassification_type_page
    acclassification_type_page = acclassification_type_page

    pass