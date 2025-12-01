from langchain.tools import tool
from langchain.agents import create_agent
from config.agent_config import SUPERVISOR_PROMPT
from agents.retriever_agent import get_retriever_agent
from tools.history import get_tools_history
from agents.response_improver_agent import get_response_improver_agent
from storage.global_store import get_global_store
from core.llm import get_llm    


@tool
def retrieve_tools(request: str):
    """
    Retrieve ERPsim specific tools according to the query.
    """
    print(f"Retriever DEBUG: request {request}")
    retriever_agent = get_retriever_agent()
    result = retriever_agent.invoke({
            "messages": [{"role": "user", "content": request}]
    })
    print(f"Retriever DEBUG: result {result['messages'][-1].text}")
    return result["messages"][-1].text


@tool
def improve_answer(request: str):
    """
    Improve response, make sure the response is educational and supported by facts.
    """
    print(f"Improver DEBUG: request {request}")
    response_improver = get_response_improver_agent()
    result = response_improver.invoke({
            "messages": [{"role": "user", "content": request}]
    })
    return result["messages"][-1].text


def get_supervisor_agent():
    """
    Create supervisor agent with relevant tools.
    """
    supervisor_agent = create_agent(
        model = get_llm(),
        tools = [retrieve_tools, get_tools_history, improve_answer],
        system_prompt =SUPERVISOR_PROMPT,
        store = get_global_store(),
    )
    return supervisor_agent