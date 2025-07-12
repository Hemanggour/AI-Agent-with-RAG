from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()


def get_gemini_embeddings():
    return GoogleGenerativeAIEmbeddings(model="models/embedding-001")
