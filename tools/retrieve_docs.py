from langchain.tools import tool, ToolRuntime
from storage.global_store import get_global_store
from config.agent_config import MAX_RETRIEVAL
from tools.helpers import get_retrieve_call_count, increment_retrieve_call_count
from storage.database import QdrantRAG
from datetime import datetime


@tool
def retrieve_documents(
    request: str,
    runtime: ToolRuntime,
    limit: int = 2
) -> str:
    """
    Retrieve general ERPsim specific game rules
    """
    config = runtime.config
    user_id = config.get("configurable", {}).get("user_id")
    if not user_id:
        raise ValueError("user_id is missing in runtime.config['configurable']")
    namespace = ("retrieved_tools", user_id)
    store = get_global_store()
    retrieve_call_count = get_retrieve_call_count(store, user_id)
    if retrieve_call_count >= MAX_RETRIEVAL:
      print("Maximum retrieval reached.")
      return f"⚠️ retrieve_tools has already been called {retrieve_call_count} times. Please reuse existing data."
    else:
      increment_retrieve_call_count(store, user_id)
      
    vector_db = QdrantRAG()
    contents = vector_db.search(request)
    result = ""

    # Check if this content has already been stored
    existing_items = store.search(namespace, "/Manufacturing_Intro.txt")
    for item in existing_items:
        print(f"🔧 Existing item DEBUG: Item: key={item.key}, value={item.value}")
        for i, content in enumerate(contents):
            if i <= limit:
                if item.value.get("content") == content:
                  print(f"🧠 Content already retrieved, skipping store.")

    for i, content in enumerate(contents):
        if i <= limit:
              # Store new content
              timestamp_key = str(datetime.now().timestamp())
              new_content = {
                "ts": datetime.now().isoformat(),
                "content": content
              }
              print(f"retrieved contents:\n {content}\n")
              store.put(namespace, timestamp_key, new_content)
              print(f"🔍 New content stored for user {user_id}")
              result += content+"\n"

    new_items = store.search(namespace)
    print(f"🔧 DEBUG: Final result: {result}")
    if not result.strip():
        result = "No new content retrieved."
    return result
  
@tool
def retrieve_sap_transactions(
    request: str,
    runtime: ToolRuntime,
    limit: int = 2
) -> str:
    """
    Retrieve general ERPsim specific game rules
    """
    config = runtime.config
    user_id = config.get("configurable", {}).get("user_id")
    if not user_id:
        raise ValueError("user_id is missing in runtime.config['configurable']")
    namespace = ("retrieved_tools", user_id)
    store = get_global_store()
    retrieve_call_count = get_retrieve_call_count(store, user_id)
    if retrieve_call_count >= MAX_RETRIEVAL:
      print("Maximum retrieval reached.")
      return f"⚠️ retrieve_tools has already been called {retrieve_call_count} times. Please reuse existing data."
    else:
      increment_retrieve_call_count(store, user_id)
      
    vector_db = QdrantRAG()
    contents = vector_db.search(request)
    print(f"Retrieved Contents: {contents}")
    result = ""

    # Check if this content has already been stored
    existing_items = store.search(namespace, "/SAP_Transaction_Manufact.txt")
    for item in existing_items:
        print(f"🔧 Existing item DEBUG: Item: key={item.key}, value={item.value}")
        for i, content in enumerate(contents):
            if i <= limit:
                if item.value.get("content") == content:
                  print(f"🧠 Content already retrieved, skipping store.")

    for i, content in enumerate(contents):
        if i <= limit:
              # Store new content
              timestamp_key = str(datetime.now().timestamp())
              new_content = {
                "ts": datetime.now().isoformat(),
                "content": content
              }
              print(f"retrieved contents:\n {content}\n")
              store.put(namespace, timestamp_key, new_content)
              print(f"🔍 New content stored for user {user_id}")
              result += content+"\n"

    store.search(namespace)
    print(f"🔧 DEBUG: Final result: {result}")
    if not result.strip():
        result = "No new content retrieved."
    return result