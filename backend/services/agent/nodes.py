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


# 2. Condition: Is the query related to Indian accountancy?
def check_indian_accountancy_topic_condition(state):
    """Determine if the query is related to Indian accountancy"""
    message = state["message"]

    # Use LLM to intelligently determine if query is Indian accountancy related
    system_prompt = """You are an AI assistant that determines whether a user's question is related to Indian accountancy.

    Indian accountancy topics include:
    - Indian Accounting Standards (Ind AS)
    - Companies Act 2013 and related accounting provisions
    - Income Tax Act provisions and tax accounting
    - GST (Goods and Services Tax) accounting and compliance
    - Financial reporting standards in India
    - Auditing standards and procedures in India
    - Indian GAAP (Generally Accepted Accounting Principles)
    - Corporate governance and compliance in India
    - Financial statement preparation and presentation
    - Cost accounting and cost audit
    - Internal audit and risk management
    - Taxation laws and their accounting implications
    - Banking and financial services accounting
    - Industry-specific accounting (manufacturing, services, etc.)
    - Professional accounting bodies (ICAI, ICWA, ICSI) guidelines
    - Accounting software and systems used in India
    - Foreign Exchange Management Act (FEMA) accounting
    - Merger and acquisition accounting
    - Valuation and fair value accounting
    - Accounting for government grants and subsidies
    - Non-profit organization accounting
    - Partnership and LLP accounting
    - Depreciation methods and asset accounting
    - Inventory valuation and management
    - Cash flow statements and fund flow analysis

    Analyze the user's question and determine if it's related to Indian accountancy in any way.

    Answer with only 'ACCOUNTANCY_RELATED' if the question is about Indian accountancy,
    or 'NOT_ACCOUNTANCY_RELATED' if it's about other topics."""

    prompt = f"{system_prompt}\n\nQuestion: {message}\n\nCategory:"

    result = llm.invoke(prompt).content.strip().upper()

    if "ACCOUNTANCY_RELATED" in result:
        return "accountancy_related"
    else:
        return "not_accountancy_related"


# 3. Polite refusal for non-Indian accountancy topics
def polite_refusal(state):
    """Generate a polite refusal for non-Indian accountancy topics"""
    refusal_message = """I'm sorry, but I'm specifically designed to assist with Indian accountancy related topics only.

I can help you with questions about:
- Indian Accounting Standards (Ind AS)
- Companies Act 2013 and accounting provisions
- Income Tax Act and tax accounting
- GST accounting and compliance
- Financial reporting standards in India
- Auditing standards and procedures
- Indian GAAP and accounting principles
- Corporate governance and compliance
- Financial statement preparation
- Cost accounting and audit
- Internal audit and risk management
- Taxation laws and accounting implications
- Banking and financial services accounting
- Professional accounting guidelines (ICAI, ICWA, ICSI)
- And much more related to Indian accountancy

Please feel free to ask me anything about Indian accountancy, and I'll be happy to help!"""

    state["response"] = refusal_message
    state["satisfied"] = True
    return state


# 4. RAG tool node
def call_rag_tool(state):
    """Retrieve relevant documents using RAG"""
    query = state["query"]
    docs = retriever.get_relevant_documents(query)

    # Combine document content
    context = "\n\n".join([doc.page_content for doc in docs])
    state["context"] = context
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

Answer with only 'SUFFICIENT' if the context is adequate, or 'INSUFFICIENT' if more or different information is needed."""

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

    system_prompt = """You are optimizing a search query to retrieve better information from an Indian accountancy knowledge base.

    The previous query didn't return sufficient information. Create a new search query that:
    - Uses different keywords or synonyms related to Indian accountancy
    - Focuses on specific aspects of the question
    - Might retrieve more relevant documents from the Indian accountancy domain

    Provide only the improved search query, nothing else."""

    prompt = f"""{system_prompt}

Original question: {state['message']}
Previous query: {state['query']}
Previous context (insufficient): {state['context'][:500]}...

Improved search query:"""

    new_query = llm.invoke(prompt).content.strip()
    state["query"] = new_query

    return state


# 7. LLM tool node - refines RAG response with context
def call_llm_tool(state):
    """Use LLM to refine the response using RAG context"""

    system_prompt = """You are an expert assistant specializing in Indian accountancy standards and related topics.

    Use the provided context to answer the user's question accurately and comprehensively.

    Guidelines:
    - Base your answer primarily on the provided context
    - If the context doesn't fully address the question, acknowledge the limitations
    - Provide clear, structured responses
    - Include specific details when available
    - Keep responses concise but informative
    - Focus on Indian accountancy aspects
    - Reference relevant Indian accounting standards, acts, and regulations when applicable"""

    prompt = f"""{system_prompt}

Question: {state['message']}

Context:
{state['context']}

Answer:"""

    response = llm.invoke(prompt)
    state["response"] = response.content.strip()
    state["satisfied"] = True

    return state


# Note: You'll also need to update the should_use_tool_condition function 
# in your graph.py to use the new function name
def should_use_tool_condition(state):
    """Determine whether to use RAG tool or LLM tool based on topic relevance"""
    topic_check = check_indian_accountancy_topic_condition(state)
    
    if topic_check == "accountancy_related":
        return "use_rag"
    else:
        return "use_llm_tool"


# Alternative function name for consistency with your graph.py
def generate_rag_answer(state):
    """Generate final answer using RAG context - alias for call_llm_tool"""
    return call_llm_tool(state)