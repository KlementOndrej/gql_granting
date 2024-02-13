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


test_reference_documents = createResolveReferenceTest(
    tableName="aclessons",
    gqltype="AclessonsGQLModel",
    attributeNames=["id", "name", "lastchange", "authorId", "description"],
)
test_query_by_id = createByIdTest(
    tableName="documents", queryEndpoint="aclessonsById"
)
test_query_page = createPageTest(
    tableName="documents", queryEndpoint="documentsPage"
)


@pytest.mark.asyncio
async def test_document_mutation():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    topic_id = "ce250b44-b095-11ed-9bd8-0242ac110002"
    description = "Pytest description"

    query = """
            mutation(
                $topic_id: UUID!
                $type_id: UUID!
                ) {
                operation: aclessonInsert(aclesson: {
                    topic_id: $topic_id    
                    description: $description
                }){
                    msg
                    entity: aclesson {
                        id
                        name
                        lastchange
                    }
                }
            }
        """

    context_value = await createContext(async_session_maker)
    variable_values = {"topic_id": topic_id, "description": description}

    resp = await schema.execute(
        query, context_value=context_value, variable_values=variable_values
    )

    print(resp, flush=True)
    assert resp.errors is None
    data = resp.data["operation"]
    assert data["msg"] == "Ok"
    data = data["entity"]
    assert data["topic_id"] == topic_id

    id = data["id"]
    lastchange = data["lastchange"]

    topic_id = "ce250b44-b095-11ed-9bd8-0242ac110003"
    query = """
            mutation(
                $id: ID!,
                $lastchange: DateTime!
                $name: UUID! topic_id!!!!
                ) {
                operation: aclessonUpdate(document: {
                id: $id,
                lastchange: $lastchange
                name: $name !!!!!!
            }){
                id
                msg
                entity: aclesson {
                    id
                    topic_id
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
    assert data["topic_id"] == topic_id

    # lastchange je jine, musi fail
    resp = await schema.execute(
        query, context_value=context_value, variable_values=variable_values
    )
    assert resp.errors is None
    data = resp.data["operation"]
    assert data["msg"] == "OK"

    pass