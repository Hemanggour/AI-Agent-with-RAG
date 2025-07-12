from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_experimental.text_splitter import SemanticChunker

from .embeddings import get_gemini_embeddings

CHROMA_PATH = "vectorstore"


def load_and_index_docs(doc_path: str):
    # Load PDF
    loader = PyMuPDFLoader(doc_path)
    pages = loader.load()

    page_texts = [doc.page_content for doc in pages]

    # Set up embedding model
    embeddings = get_gemini_embeddings()

    chunker = SemanticChunker(
        embeddings,
        breakpoint_threshold_type="percentile",
        breakpoint_threshold_amount=90,
    )

    chunks = chunker.create_documents(page_texts)

    vectordb = Chroma.from_documents(
        documents=chunks, embedding=embeddings, persist_directory=CHROMA_PATH
    )
    vectordb.persist()
    print("Vector store created.")


def get_retriever():
    embeddings = get_gemini_embeddings()
    vectordb = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    return vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 5})
