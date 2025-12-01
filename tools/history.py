from langchain.tools import tool, ToolRuntime
from storage.global_store import get_global_store
import json

@tool
def get_tools_history(runtime: ToolRuntime):
    """
    Retrieves past retrievals for the current user.
    """
    config = runtime.config
    user_id = config["configurable"].get("user_id")
    namespace = ("retrieved_tools", user_id)
    store = get_global_store()
    items = store.search(namespace)
    history = [item.value for item in items]
    if len(history) == 0:
        return "No previous tool history found."
    return json.dumps(history, ensure_ascii=False)