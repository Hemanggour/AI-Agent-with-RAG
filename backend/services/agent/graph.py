from typing import Optional, TypedDict

from langgraph.graph import END, StateGraph

from .nodes import (
    analyze_question,
    call_rag_tool,
    check_context_relevance_condition,
    generate_final_answer,
    refine_query,
    should_use_tool_condition,
)


class AgentState(TypedDict):
    message: str
    response: Optional[str] = None
    query: Optional[str] = None
    context: Optional[str] = None
    tool_calls: Optional[int] = None
    satisfied: Optional[bool] = None


def get_langgraph():
    builder = StateGraph(AgentState)

    # Add all nodes
    builder.add_node("analyze_question", analyze_question)
    builder.add_node("call_rag_tool", call_rag_tool)
    builder.add_node("refine_query", refine_query)
    builder.add_node("generate_final_answer", generate_final_answer)

    # Set entry point
    builder.set_entry_point("analyze_question")

    # Add conditional edges - these functions return the next node name
    builder.add_conditional_edges(
        "analyze_question",
        should_use_tool_condition,
        {"use_tool": "call_rag_tool", "skip_tool": "generate_final_answer"},
    )

    builder.add_conditional_edges(
        "call_rag_tool",
        check_context_relevance_condition,
        {"relevant": "generate_final_answer", "not_relevant": "refine_query"},
    )

    # Add regular edges
    builder.add_edge("refine_query", "call_rag_tool")
    builder.add_edge("generate_final_answer", END)

    return builder.compile()
