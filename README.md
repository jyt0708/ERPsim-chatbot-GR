# ERPsim-chatbot-GR
sequenial_retireval_with_reasoning:
The graph uses one reasoning agent (or LLM) that operates through a state machine (LangGraph) with different nodes representing processing steps or function calls. Each node (like generate_query_or_respond, retrieve, generate_answer, etc.) is a function executed by the same agent or pipeline, not separate agents with their own goals or memory. (Single Agent)
All logic flows through a single decision graph.
