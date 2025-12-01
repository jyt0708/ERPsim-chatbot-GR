from typing import TypedDict, Literal


# State for tracking the evaluation
class ERPState(TypedDict):
    user_query: str
    response: str
    # context: str
    status: Literal["good", "bad"]
    evaluation_feedback: str
    config: dict