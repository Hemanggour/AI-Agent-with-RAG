from typing import Optional, TypedDict
from langgraph.graph import END, StateGraph
from .nodes import (
    analyze_question,
    call_llm_tool,
    call_rag_tool,
    check_context_relevance_condition,
    generate_rag_answer,
    refine_query,
    should_use_tool_condition,
    polite_refusal,
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
    builder.add_node("call_llm_tool", call_llm_tool)
    builder.add_node("refine_query", refine_query)
    builder.add_node("generate_rag_answer", generate_rag_answer)
    builder.add_node("polite_refusal", polite_refusal)

    # Set entry point
    builder.set_entry_point("analyze_question")

    # Add conditional edges - route to RAG for Indian accountancy or polite refusal for other topics
    builder.add_conditional_edges(
        "analyze_question",
        should_use_tool_condition,
        {
            "use_rag": "call_rag_tool",
            "use_llm_tool": "polite_refusal",
        },
    )

    # RAG tool flow (unchanged)
    builder.add_conditional_edges(
        "call_rag_tool",
        check_context_relevance_condition,
        {"relevant": "generate_rag_answer", "not_relevant": "refine_query"},
    )

    # Add regular edges
    builder.add_edge("refine_query", "call_rag_tool")
    builder.add_edge("generate_rag_answer", END)

    # Polite refusal goes directly to END
    builder.add_edge("polite_refusal", END)

    return builder.compile()
