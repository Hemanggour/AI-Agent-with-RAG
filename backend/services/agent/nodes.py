from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from backend.services.rag import get_retriever

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.2)
retriever = get_retriever()

# Maximum number of RAG calls to prevent infinite loops
MAX_TOOL_CALLS = 3


# 1. Analyze user question and create an initial RAG query
def analyze_question(state):
    """Initialize the state with user query and reset counters"""
    state["query"] = state["message"]
    state["tool_calls"] = 0
    state["satisfied"] = False
    return state


# 2. Condition: Should the LLM use a tool (RAG)?
def should_use_tool_condition(state):
    """Determine if RAG tool should be used based on question analysis"""
    message = state["message"]

    # Use LLM to make this decision more intelligently
    system_prompt = """You are an AI assistant that determines if a question requires retrieving information from a knowledge base.

    Analyze the user's question and determine if it:
    - Asks for specific information, facts, or explanations
    - Requires knowledge about specific topics, standards, or procedures
    - Needs contextual information to provide a complete answer

    Answer with only 'YES' if the question requires knowledge retrieval, or 'NO' if it's a general question that can be answered without specific context."""  # noqa

    prompt = f"{system_prompt}\n\nQuestion: {message}\n\nRequires knowledge retrieval:"

    result = llm.invoke(prompt).content.lower().strip()

    if "yes" in result:
        return "use_tool"
    else:
        return "skip_tool"


# 3. RAG tool node
def call_rag_tool(state):
    """Retrieve relevant documents using RAG"""
    query = state["query"]
    docs = retriever.get_relevant_documents(query)

    # Combine document content
    context = "\n\n".join([doc.page_content for doc in docs])
    state["context"] = context
    state["tool_calls"] += 1

    return state


# 4. Condition: Is the retrieved context relevant and sufficient?
def check_context_relevance_condition(state):
    """Check if the retrieved context is sufficient to answer the question"""

    # Prevent infinite loops
    if state["tool_calls"] >= MAX_TOOL_CALLS:
        return "relevant"

    system_prompt = """You are evaluating whether the provided context contains sufficient information to answer the user's question accurately and completely.

    Consider:
    - Does the context directly address the question?
    - Is there enough detail to provide a comprehensive answer?
    - Is the information relevant and up-to-date?

    Answer with only 'SUFFICIENT' if the context is adequate, or 'INSUFFICIENT' if more or different information is needed."""  # noqa

    prompt = f"""{system_prompt}

Question: {state['message']}

Context:
{state['context']}

Context assessment:"""

    result = llm.invoke(prompt).content.lower().strip()

    if "sufficient" in result:
        return "relevant"
    else:
        return "not_relevant"


# 5. Refine query for better RAG results
def refine_query(state):
    """Generate a better search query based on previous results"""

    system_prompt = """You are optimizing a search query to retrieve better information from a knowledge base.

    The previous query didn't return sufficient information. Create a new search query that:
    - Uses different keywords or synonyms
    - Focuses on specific aspects of the question
    - Might retrieve more relevant documents

    Provide only the improved search query, nothing else."""  # noqa

    prompt = f"""{system_prompt}

Original question: {state['message']}
Previous query: {state['query']}
Previous context (insufficient): {state['context'][:500]}...

Improved search query:"""

    new_query = llm.invoke(prompt).content.strip()
    state["query"] = new_query

    return state


# 6. Generate final answer
def generate_final_answer(state):
    """Generate the final response using available context"""

    if state.get("context"):
        # Answer using context
        system_prompt = """You are an expert assistant specializing in Indian Accounting Standards and related topics.

        Use the provided context to answer the user's question accurately and comprehensively.

        Guidelines:
        - Base your answer primarily on the provided context
        - If the context doesn't fully address the question, acknowledge the limitations
        - Provide clear, structured responses
        - Include specific details when available"""  # noqa

        prompt = f"""{system_prompt}

Question: {state['message']}

Context:
{state['context']}

Answer:"""
    else:
        # Answer without context (for simple questions)
        system_prompt = """You are an expert assistant. Answer the user's question based on your general knowledge.

        Provide a helpful, accurate response. If you're not certain about specific details, acknowledge the uncertainty."""  # noqa

        prompt = f"""{system_prompt}

Question: {state['message']}

Answer:"""

    response = llm.invoke(prompt)
    state["response"] = response.content.strip()
    state["satisfied"] = True

    return state
