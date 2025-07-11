from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END
from .nodes import retrieve_docs, build_prompt, llm_inference

# Define state schema
class AgentState(TypedDict):
    message: str
    response: Optional[str] = None
    context: Optional[str] = None
    final_prompt: Optional[str] = None


def get_langgraph():
    builder = StateGraph(AgentState)

    # Define nodes
    builder.add_node("retrieve_docs", retrieve_docs)
    builder.add_node("build_prompt", build_prompt)
    builder.add_node("llm_inference", llm_inference)

    # Define flow
    builder.set_entry_point("retrieve_docs")
    builder.add_edge("retrieve_docs", "build_prompt")
    builder.add_edge("build_prompt", "llm_inference")
    builder.add_edge("llm_inference", END)

    return builder.compile()
