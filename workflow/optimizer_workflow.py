from langgraph.graph import StateGraph, START, END
from core.state import ERPState
from agents.evaluator_agent import supervisor_response_node, response_evaluator_node, route_response


def get_optimizer_workflow():
    optimizer_builder = StateGraph(ERPState)

    optimizer_builder.add_node("SupervisorResponseNode", supervisor_response_node)
    optimizer_builder.add_node("ResponseEvaluatorNode", response_evaluator_node)

    optimizer_builder.add_edge(START, "SupervisorResponseNode")
    optimizer_builder.add_edge("SupervisorResponseNode", "ResponseEvaluatorNode")
    optimizer_builder.add_conditional_edges(
        "ResponseEvaluatorNode",
        route_response,
        {
            "End": END,
            "SupervisorResponseNode": "SupervisorResponseNode"
        }
    )

    optimizer_workflow = optimizer_builder.compile()
    return optimizer_workflow