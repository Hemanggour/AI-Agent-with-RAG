# nodes.py

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from backend.services.rag import get_retriever

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.8)
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


# 2. Condition: Should the LLM use a tool (RAG or LLM)?
def should_use_tool_condition(state):
    """Determine if RAG tool, LLM tool, or direct answer should be used"""
    message = state["message"]

    # Use LLM to make this decision more intelligently
    system_prompt = """You are an AI assistant that determines the best approach to answer a user's question.

    Analyze the user's question and categorize it as:
    1. RAG_REQUIRED - Questions that need specific information from a knowledge base (facts, standards, procedures, specific domain knowledge)
    2. LLM_TOOL - Questions that need general reasoning, analysis, calculations, or creative responses but don't require specific knowledge retrieval
    3. DIRECT - Simple questions that can be answered directly without tools

    Examples:
    - "What is the accounting standard for inventory?" → RAG_REQUIRED
    - "Can you analyze this financial data and provide insights?" → LLM_TOOL
    - "Hello, how are you?" → DIRECT

    Answer with only one of: RAG_REQUIRED, LLM_TOOL, or DIRECT"""  # noqa

    prompt = f"{system_prompt}\n\nQuestion: {message}\n\nCategory:"

    result = llm.invoke(prompt).content.strip().upper()

    if "RAG_REQUIRED" in result:
        return "use_rag"
    elif "LLM_TOOL" in result:
        return "use_llm_tool"
    else:
        return "direct_answer"


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


# 4. LLM tool node
def call_llm_tool(state):
    """Use LLM as a tool for reasoning, analysis, or creative tasks"""
    print("Using LLM call tool")
    system_prompt = """You are an expert AI assistant with advanced reasoning capabilities.

    The user has asked a question that requires:
    - Analysis or reasoning
    - Creative thinking
    - Problem-solving
    - Calculations or logical processing
    - General knowledge application

    Provide a comprehensive, well-structured response that addresses the user's question thoroughly.
    Use your knowledge and reasoning capabilities to give the best possible answer."""

    prompt = f"""{system_prompt}

User Question: {state['message']}

Please provide a detailed response:"""

    response = llm.invoke(prompt)
    state["llm_tool_response"] = response.content.strip()
    state["tool_calls"] += 1

    return state


# 5. Condition: Is the retrieved context relevant and sufficient?
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


# 6. Refine query for better RAG results
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


# 7. Generate final answer with RAG context
def generate_rag_answer(state):
    """Generate the final response using RAG context"""

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

    response = llm.invoke(prompt)
    state["response"] = response.content.strip()
    state["satisfied"] = True

    return state


# 8. Generate final answer with LLM tool response
def generate_llm_tool_answer(state):
    """Generate the final response using LLM tool output"""

    # The LLM tool has already generated a response, so we can use it directly
    # or optionally refine it further

    system_prompt = """You are reviewing and potentially refining a response generated by an AI tool.

    The response should be:
    - Accurate and helpful
    - Well-structured and clear
    - Appropriate for the user's question

    If the response is already good, return it as is. If it needs refinement, improve it."""  # noqa

    prompt = f"""{system_prompt}

Original Question: {state['message']}

Generated Response:
{state['llm_tool_response']}

Final Response:"""

    response = llm.invoke(prompt)
    state["response"] = response.content.strip()
    state["satisfied"] = True

    return state


# 9. Generate direct answer
def generate_direct_answer(state):
    """Generate a direct response for simple questions"""

    system_prompt = """You are a helpful AI assistant. Answer the user's question directly and concisely.

    For simple questions, provide a straightforward response without unnecessary complexity."""  # noqa

    prompt = f"""{system_prompt}

Question: {state['message']}

Answer:"""

    response = llm.invoke(prompt)
    state["response"] = response.content.strip()
    state["satisfied"] = True

    return state
