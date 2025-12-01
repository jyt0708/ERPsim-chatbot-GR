from storage.global_store import get_global_store
from agents.supervisor_agent import get_supervisor_agent
from core.llm import get_llm    
from core.state import ERPState
from config.agent_config import DETAIL_INSTRUCTIONS


def supervisor_response_node(state: ERPState):
    """Supervisor agent generates a response to user query"""

    # Include evaluator feedback in prompt if it exists
    prompt_content = state["user_query"]
    if state.get("evaluation_feedback"):
        prompt_content += (
        f"\nPrevious response was rejected. Use the following evaluator reasoning to improve your response:\n"
        f"{state['evaluation_feedback']}\n"
        f"Generate a new response that addresses all issues mentioned above."
        )
    
    print("Prompt passed to supervisor:")
    print(prompt_content)
    
    supervisor_agent = get_supervisor_agent()
    stream = supervisor_agent.stream(
        {"messages": [{"role": "user", "content": prompt_content}]},
        config=state.get("config")
    )

    last_response = ""
    for step in stream:
        for update in step.values():
            for message in update.get("messages", []):
                message.pretty_print()
                print(f"Supervisor agent reasoning content: {message.additional_kwargs.get('reasoning_content')}")
                if message.content.strip():  # only update if not empty
                    last_response += message.content +"\n"

    state['evaluation_feedback'] = ""
    
    return {"response": last_response}


# Evaluator checks the response
def response_evaluator_node(state: ERPState):
    """Evaluate the response for relevance, completeness, and length"""
    print(f"Evaluator node")
    response = state["response"]
    query = state["user_query"]
    store = get_global_store()
    namespace = ("retrieved_tools", 'user_123')
    existing_items = store.search(namespace)
    retrieved_content = ""
    for item in existing_items:
        value = item.value
        if value and value.get("content"):
            retrieved_content += f"\n- {value['content']}"
            
    level = state["config"]["configurable"].get("level", "medium") 
    
    prompt = f"""
    Evaluate the following supervisor response based on the user query.

    User query:
    {query}

    Retrieved Content:
    {retrieved_content}

    Generated Response:
    {response}

    Criteria:
    1. The response must be relevant to the user query.
    2. The response must adhere to the retrieved content and does not contain fabricated content.
    2. The response must completely answer the query.
    3. The response must not be unnecessarily long.
    4. The response must be educational and easy for students to understand and follow.
    5. {DETAIL_INSTRUCTIONS[level]}.

    Decide if the response is 'good' or 'bad'. Only response with 'good' or 'bad.'
    """
     
    llm_model = get_llm() 
    result = llm_model.invoke(prompt)
    grade = result.content
    reason = result.additional_kwargs.get('reasoning_content')

    return {
        "status": grade,
        "evaluation_feedback": reason
    }


def route_response(state: ERPState):
    if state["status"] == "good":
        return "End"
    elif state["status"] == "bad":
        return "SupervisorResponseNode"