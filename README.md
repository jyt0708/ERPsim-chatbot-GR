# Multi-agent workflow with Supervisor and Evaluator
The supervisor agent is responsible for calling tools and agents, it will provide the answer to the evaluator once it thinks its response is good enough. The evaluator agent will decide whether to 
provide the final answer to the user based on i) educational meaning, ii) level check, iii) context adherence.

## Project Structure
```text
ERPsim-chatbot-GR/
├── .gitignore
├── README.md
├── Manufacturing_Intro.txt
├── SAP_Transaction_Manufact.txt
├── main.py
├── requirements.txt
├── agents/
│   ├── __init__.py
│   ├── agent_base.py
│   ├── agent_x.py
│   └── …  (other agent modules)
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── credentials_example.yaml
│   └── … (other config files)
├── core/
│   ├── __init__.py
│   ├── engine.py
│   ├── processing.py
│   └── … (core logic modules)
├── storage/
│   ├── __init__.py
│   ├── db.py
│   ├── models.py
│   └── … (storage/back‑end modules)
├── tools/
│   ├── __init__.py
│   ├── util.py
│   ├── helper.py
│   └── … (utility or helper modules)
├── workflow/
│   ├── __init__.py
│   ├── workflow_manager.py
│   ├── task_queue.py
│   └── … (workflow related modules)
