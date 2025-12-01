import uuid
from storage.database import QdrantRAG
from langgraph.store.memory import InMemoryStore
from storage.global_store import initialize_store
from workflow.optimizer_workflow import get_optimizer_workflow
from storage.global_odata_manager import ensure_odata_manager


vector_db = QdrantRAG()
# vector_db.remove_collection("hybrid")
initialize_store(InMemoryStore())

odata_manager = ensure_odata_manager(
    url="https://e05.bi.ucc.cit.tum.de/odata/942",  
    username="A_2",
    password="WatsonX2027"
)


config = {
    "configurable": {
        "thread_id": str(uuid.uuid4()),
        "user_id": "user_123",
        "level": "low"
    }
}
optimizer_workflow = get_optimizer_workflow()
state = optimizer_workflow.invoke({
    "user_query": "Based on my current game state, how to improve profit?",
    "config": config
})

print("\nFinal Response:\n", state["response"])





