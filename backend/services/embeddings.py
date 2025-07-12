from dotenv import load_dotenv
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings

load_dotenv()


def get_gemini_embeddings():
    return GoogleGenerativeAIEmbeddings(model="models/embedding-001")
