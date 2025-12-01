from langchain.agents import create_agent
from core.llm import get_llm
from storage.global_store import get_global_store
from tools.improve_and_factualize import improve_quality, factualize_response
from config.agent_config import REPONSE_IMPROVER_PROMPT

def get_response_improver_agent():
    response_improver = create_agent(
        model=get_llm(),
        tools=[improve_quality, factualize_response],
        store=get_global_store(),
        system_prompt=REPONSE_IMPROVER_PROMPT,
    )
    return response_improver