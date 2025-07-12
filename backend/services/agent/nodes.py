from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from backend.services.rag import get_retriever

from .prompt import get_prompt_template

load_dotenv()

retriever = get_retriever()
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.2)
prompt_template = get_prompt_template()


def retrieve_docs(state):
    query = state["message"]
    docs = retriever.invoke(query)
    context = "\n\n".join([doc.page_content for doc in docs])
    state["context"] = context
    return state


def build_prompt(state):
    state["final_prompt"] = prompt_template.format(
        context=state["context"], question=state["message"]
    )
    return state


def llm_inference(state):
    print(f"CONTEXT:\n{state["context"]}\n")
    response = llm.invoke(state["final_prompt"])
    state["response"] = response.content
    return state
