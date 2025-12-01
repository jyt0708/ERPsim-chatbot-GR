# Multi-agent workflow with Supervisor and Evaluator
The supervisor agent is responsible for calling tools and agents, it will provide the answer to the evaluator once it thinks its response is good enough. The evaluator agent will decide whether to 
provide the final answer to the user based on i) educational meaning, ii) level check, iii) context adherence.

## Project Structure
```text
ERPsim-chatbot-GR/
├── agents/
│   ├── __init__.py
│   ├── evaluator_agent.py            # Agent that evaluates the final response 
│   ├── response_improver_agent.py    # Agent that improves response quality
│   ├── retriever_agent.py            # Agent that retrieves data and information
│   └── supervisor_agent.py           # Agent that decides which agent/tool to call
├── config/
│   ├── __init__.py       
│   └── agent_config.py              # Prompts and general settings
├── core/
│   ├── __init__.py
│   ├── llm.py                      # Manages LLM instances
│   └── state.py                    # Main ERPState definition (for LangGraph)
├── storage/
│   ├── __init__.py
│   ├── database.py                # QDrant client, collection management, querying
│   ├── global_odata_manager.py      # The only OData manager used in the whole chat
│   ├── global_store.py              # Persist knowledge (retrieved context) over time
│   └── odata_source.py              #  Connects to an OData API, automatically generates tools for each entity
├── tools/
│   ├── __init__.py
│   ├── helpers.py                  # Helper functions for the tools
│   ├── history.py                  # A tool that retrieves past retrievals for the current session
│   ├── improve_and_factualize.py    # A tool that improves the quality of the response
│   ├── odata_tools.py               # A tool that retrieves odata entity
│   └── retrieve_docs.py             # A tool that retrieves game spesific static data
├── workflow/
│   ├── __init__.py
│   └── optimizer_workflow.py        # LangGraph supervisor-evaluator workflow
├── .gitignore
├── README.md
├── Manufacturing_Intro.txt
├── SAP_Transaction_Manufact.txt
├── main.py        # Main application code
└──  requirements.txt
