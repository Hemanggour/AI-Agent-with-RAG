from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from .embeddings import get_gemini_embeddings

CHROMA_PATH = "vectorstore"


def load_and_index_docs(doc_path: str = "data/Indian-Accounting-Standards-IND-AS.pdf"):
    # Load PDF
    loader = PyMuPDFLoader(doc_path)
    docs = loader.load()

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
    chunks = splitter.split_documents(docs)

    # Embed with Gemini
    embeddings = get_gemini_embeddings()

    # Store in Chroma
    vectordb = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=CHROMA_PATH)
    vectordb.persist()
    print("Vector store created.")


def get_retriever():
    embeddings = get_gemini_embeddings()
    vectordb = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    return vectordb.as_retriever()
