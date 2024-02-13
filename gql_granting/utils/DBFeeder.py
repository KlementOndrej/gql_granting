from doctest import master
from functools import cache
from gql_granting.DBDefinitions import BaseModel

import random
import itertools
from functools import cache


from sqlalchemy.future import select


def singleCall(asyncFunc):
    """Dekorator, ktery dovoli, aby dekorovana funkce byla volana (vycislena) jen jednou. Navratova hodnota je zapamatovana a pri dalsich volanich vracena.
    Dekorovana funkce je asynchronni.
    """
    resultCache = {}

    async def result():
        if resultCache.get("result", None) is None:
            resultCache["result"] = await asyncFunc()
        return resultCache["result"]

    return result

import datetime

from gql_granting.DBDefinitions import (
    
    ProgramFormTypeModel,
    ProgramLanguageTypeModel,
    ProgramLevelTypeModel,
    ProgramTitleTypeModel,
    ProgramTypeModel,
    ProgramModel,
    SubjectModel,
    SemesterModel,
    TopicModel,
    LessonModel,
    LessonTypeModel,
    
    ClassificationLevelModel,
    ClassificationModel,
    ClassificationTypeModel,

    ProgramStudents,
)

import asyncio
import os
import json
import uuid

from uoishelpers.feeders import ImportModels

def get_demodata():
    def datetime_parser(json_dict):
        for (key, value) in json_dict.items():
            if key in ["startdate", "enddate", "lastchange", "created"]:
                if value is None:
                    dateValueWOtzinfo = None
                else:
                    try:
                        dateValue = datetime.datetime.fromisoformat(value)
                        dateValueWOtzinfo = dateValue.replace(tzinfo=None)
                    except:
                        print("jsonconvert Error", key, value, flush=True)
                        dateValueWOtzinfo = None
                
                json_dict[key] = dateValueWOtzinfo
            
            if (key in ["id", "changedby", "createdby"]) or (key.endswith("_id")):
                
                if key == "outer_id":
                    json_dict[key] = value
                elif value not in ["", None]:
                    json_dict[key] = uuid.UUID(value)
                else:
                    pass
                    #print(key, value)
            #if (key == "event_id"): print(key, value)

        return json_dict
    
    with open("./systemdata.json", "r", encoding="utf-8") as f:
        jsonData = json.load(f, object_hook=datetime_parser)

    return jsonData    

async def initDB(asyncSessionMaker):

    demo = os.environ.get("DEMO", None)
    if demo not in [None, "true"]:
        dbModels = [
            ProgramFormTypeModel,
            ProgramLanguageTypeModel,
            ProgramLevelTypeModel,
            ProgramTitleTypeModel,
            ProgramTypeModel,
            LessonTypeModel,

            ClassificationLevelModel,
            ClassificationTypeModel,
        ]
    else:
        dbModels = [
            ProgramFormTypeModel,
            ProgramLanguageTypeModel,
            ProgramLevelTypeModel,
            ProgramTitleTypeModel,
            ProgramTypeModel,
            LessonTypeModel,
            ClassificationLevelModel,
            ClassificationTypeModel,

            ProgramModel,
            SubjectModel,
            SemesterModel,
            TopicModel,
            LessonModel,
            ClassificationModel,
            ProgramStudents
        ]
        
    jsonData = get_demodata()
    await ImportModels(asyncSessionMaker, dbModels, jsonData)
    pass
