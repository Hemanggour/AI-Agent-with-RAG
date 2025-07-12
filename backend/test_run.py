from services.agent.graph import AgentState, get_langgraph

graph = get_langgraph()

if __name__ == "__main__":
    user_input = input("Ask me an accounting question: ")

    agent_state = AgentState(message=user_input)

    result = graph.invoke(agent_state)

    print("\nAssistant:", result["response"])
