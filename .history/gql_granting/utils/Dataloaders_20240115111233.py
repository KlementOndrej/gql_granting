from uoishelpers.dataloaders import createIdLoader, createFkeyLoader
from functools import cache

from gql_granting.DBDefinitions import (
    ProgramFormTypeModel,
    ProgramGroupModel,
    ProgramLanguageTypeModel,
    ProgramLevelTypeModel,
    ProgramModel,
    ProgramTitleTypeModel,
    ProgramTypeModel,
    ProgramStudents,

    ClassificationLevelModel,
    ClassificationModel,
    ClassificationTypeModel,
    
    SubjectModel,
    SemesterModel,
    TopicModel,
    LessonModel,
    LessonTypeModel
)
async def createLoaders_3(asyncSessionMaker):

    class Loaders:
        @property
        @cache
        def acprogramform(self):
            return createIdLoader(asyncSessionMaker, ProgramFormTypeModel)

        @property
        @cache
        def acprogramlanguage(self):
            return createIdLoader(asyncSessionMaker, ProgramLanguageTypeModel)

        @property
        @cache
        def acprogramlevel(self):
            return createIdLoader(asyncSessionMaker, ProgramLevelTypeModel)

        @property
        @cache
        def acprogramtitle(self):
            return createIdLoader(asyncSessionMaker, ProgramTitleTypeModel)

        @property
        @cache
        def acprogramtype(self):
            return createIdLoader(asyncSessionMaker, ProgramTypeModel)

        @property
        @cache
        def acclassificationlevel(self):
            return createIdLoader(asyncSessionMaker, ClassificationLevelModel)

        @property
        @cache
        def acclassificationtype(self):
            return createIdLoader(asyncSessionMaker, ClassificationTypeModel)

        @property
        @cache
        def aclessontype(self):
            return createIdLoader(asyncSessionMaker, LessonTypeModel)

        @property
        @cache
        def acprogramgroup(self):
            return createIdLoader(asyncSessionMaker, ProgramGroupModel)

        @property
        @cache
        def acprogram(self):
            return createIdLoader(asyncSessionMaker, ProgramModel)

        @property
        @cache
        def acsubject(self):
            return createIdLoader(asyncSessionMaker, SubjectModel)

        @property
        @cache
        def acsubjectprogram(self):
            return createFkeyLoader(asyncSessionMaker, SubjectModel, foreignKeyName="program_id")

        @property
        @cache
        def acsemestersubject(self):
            return createFkeyLoader(asyncSessionMaker, SemesterModel, foreignKeyName="subject_id")

        @property
        @cache
        def acsemester(self):
            return createIdLoader(asyncSessionMaker, SemesterModel)

        @property
        @cache
        def actopic(self):
            return createIdLoader(asyncSessionMaker, TopicModel)

        @property
        @cache
        def actopicssemester(self):
            return createFkeyLoader(asyncSessionMaker, TopicModel, foreignKeyName="semester_id")

        @property
        @cache
        def aclesson(self):
            return createIdLoader(asyncSessionMaker, LessonModel)

        @property
        @cache
        def aclessonstopic(self):
            return createFkeyLoader(asyncSessionMaker, LessonModel, foreignKeyName="topic_id")

        @property
        @cache
        def acclassification(self):
            return createIdLoader(asyncSessionMaker, ClassificationModel)

        @property
        @cache
        def acclassificationsemester(self):
            return createFkeyLoader(asyncSessionMaker, ClassificationModel, foreignKeyName="semester_id")

    return Loaders()

dbmodels = {
    "programforms": ProgramFormTypeModel,
    "programgroups": ProgramGroupModel,
    "programlanguages": ProgramLanguageTypeModel,
    "programleveltypes": ProgramLevelTypeModel,
    "programs": ProgramModel,
    "programtitletypes": ProgramTitleTypeModel,
    "programtypes": ProgramTypeModel,
    "programstudents": ProgramStudents,

    "classificationlevels": ClassificationLevelModel,
    "classifications": ClassificationModel,
    "classificationtypes": ClassificationTypeModel,
    
    "subjects": SubjectModel,
    "semesters": SemesterModel,
    "topics": TopicModel,
    "lessons": LessonModel,
    "lessontypes": LessonTypeModel
}

def createLoaders(asyncSessionMaker, models=dbmodels):
    def createLambda(loaderName, DBModel):
        return lambda self: createIdLoader(asyncSessionMaker, DBModel)
    
    attrs = {}
    for key, DBModel in models.items():
        attrs[key] = property(cache(createLambda(key, DBModel)))
    
    Loaders = type('Loaders', (), attrs)   
    return Loaders()