from langchain.tools import tool, ToolRuntime
from langchain_core.messages import HumanMessage, ToolMessage
from config.agent_config import DETAIL_INSTRUCTIONS
from storage.global_store import get_global_store
from core.llm import get_llm

@tool
def improve_quality(
    request: str,
    runtime: ToolRuntime
) -> str:
    """
    Make the answer more educational and adjust the answer detail based on the given level.
    """
    # Get the original user query (first HumanMessage)
    human_messages = [msg for msg in runtime.state["messages"] if isinstance(msg, HumanMessage)]
    if human_messages:
        original_user_message = human_messages[0].content  # First human message
    else:
        original_user_message = ""

    # Get the most recent response
    tool_messages = [msg for msg in runtime.state["messages"] if isinstance(msg, ToolMessage)]
    if tool_messages:
        recent_response = tool_messages[-1].content  # Last Tool message
    else:
        recent_response = ""

    config = runtime.config
    user_id = config["configurable"].get("user_id")
    namespace = ("retrieved_tools", user_id)
    store = get_global_store()
    existing_items = store.search(namespace)
    retrieved_content = ""
    for item in existing_items:
        value = item.value
        if value and value.get("content"):
            retrieved_content += f"\n- {value['content']}"
            
    level = config["configurable"].get("level", "medium")
    
    prompt = (
        "You are an educational assistant for ERPsim students.\n"
        "Your task: Improve the following answer so it becomes more educational and encouraging.\n"
        "Simplify technical terms, and help students understand key principles.\n"
        "The improved answer should be concise, well-structured, and limited to a maximum of five sentences.\n"
        f"{DETAIL_INSTRUCTIONS[level]}\n\n"

        f"User's question: '{original_user_message}'\n\n"

        "Context:\n"
        f"{retrieved_content}\n\n"

        "Answer to improve:\n"
        f"{recent_response}\n\n"
        
        "Please output only the improved version of this answer:"
    )

    llm_model = get_llm()
    result = llm_model.invoke([{"role": "user", "content": prompt}])
    improved_answer = getattr(result, "content", "")
    print(f"Improved answer {improved_answer}")
    return improved_answer


@tool
def factualize_response(
    request: str,
    runtime: ToolRuntime
) -> str:
    """
    Improve the answer based on retrieved context. Remove hallucinations. If the answer seems inaccurate → correct and verify
    """
    # Get the most recent response
    tool_messages = [msg for msg in runtime.state["messages"] if isinstance(msg, ToolMessage)]
    recent_response = tool_messages[-1].content if tool_messages else ""

    # Retrieve stored context
    config = runtime.config
    user_id = config["configurable"].get("user_id")
    namespace = ("retrieved_tools", user_id)
    store = get_global_store()
    existing_items = store.search(namespace)
    retrieved_content = ""
    for item in existing_items:
        value = item.value
        if value and value.get("content"):
            retrieved_content += f"\n- {value['content']}"
            
    level = config["configurable"].get("level", "medium")

    prompt = (
        "You are an educational assistant for ERPsim students.\n"
        "Your task: Improve the following answer using only the retrieved context.\n"
        "Do not invent any information. If something in the answer is not supported by the context, remove it.\n"
        "Simplify technical terms and make the explanation clear and educational.\n"
        f"{DETAIL_INSTRUCTIONS[level]}\n\n"
        f"Retrieved context:\n{retrieved_content}\n\n"

        "Answer to factualize:\n"
        f"{recent_response}\n\n"

        "Please output only the corrected, factual, and clear version of this answer:"
    )
    llm_model = get_llm()
    result = llm_model.invoke([{"role": "user", "content": prompt}])
    factual_answer = getattr(result, "content", "")
    print(f"Factualized answer {factual_answer}")
    return factual_answer