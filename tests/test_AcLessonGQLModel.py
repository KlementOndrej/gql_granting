import pytest

from .gt_utils import (
    createByIdTest,
    createPageTest,
    createResolveReferenceTest,
    prepare_in_memory_sqllite,
    prepare_demodata,
    get_demodata,
    createContext,
    schema,
)


test_reference_aclessons = createResolveReferenceTest(
    tableName="aclessons",
    gqltype="AcLessonGQLModel",
    attributeNames=["id"],
)
test_query_by_id = createByIdTest(
    tableName="aclessons", queryEndpoint="aclessonById"
)
test_query_page = createPageTest(
    tableName="aclessons", queryEndpoint="aclessonsPage"
)


@pytest.mark.asyncio
async def test_aclessons_mutation():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    topic_id = "ce250b44-b095-11ed-9bd8-0242ac110002"
    type_id = "e2b7cbf6-95e1-11ed-a1eb-0242ac120002"

    query = """
            mutation(
                $topic_id: UUID!
                $type_id: UUID!
                ) {
                operation: lessonInsert(lesson: { 
                    topicId: $topic_id    
                    typeId: $type_id
                }){
                    msg
                    entity: lesson {
                        id
                        type {id}
                        lastchange
                    }
                }
            }
        """

                #řádek 41 (lessonInsert?, aclessons?)

    context_value = await createContext(async_session_maker)
    variable_values = {"topic_id": topic_id, "type_id": type_id}

    resp = await schema.execute(
        query, context_value=context_value, variable_values=variable_values
    )

    print(resp, flush=True)
    assert resp.errors is None
    data = resp.data["operation"]
    assert data["msg"] == "Ok"
    data = data["entity"]
    assert data["type"]["id"] == topic_id

    id = data["id"]
    lastchange = data["lastchange"]

    topic_id = "ce250b44-b095-11ed-9bd8-0242ac110003"
    query = """
            mutation(
                $id: ID!,   
                $lastchange: DateTime!
                $topic_id: UUID!
                ) {
                operation: aclessonUpdate(lesson: {
                id: $id,
                lastchange: $lastchange
                topicId: $topic_id
            }){
                id
                msg
                entity: aclesson {
                    id
                    topic {id}
                    lastchange
                }
            }
            }
        """
    
    context_value = await createContext(async_session_maker)
    variable_values = {"id": id, "topic_id": topic_id, "lastchange": lastchange}
    resp = await schema.execute(
        query, context_value=context_value, variable_values=variable_values
    )
    assert resp.errors is None

    data = resp.data["operation"]
    assert data["msg"] == "ok"
    data = data["entity"]
    assert data["topic"]["id"] == topic_id

    #lastchange je jine, musi fail
    resp = await schema.execute(
        query, context_value=context_value, variable_values=variable_values
    )
    assert resp.errors is None
    data = resp.data["operation"]
    assert data["msg"] == "ok"

    pass