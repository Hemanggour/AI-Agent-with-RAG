from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routes import router

# from pyngrok import ngrok


app = FastAPI(
    title="Accounting AI Assistant",
    description="FastAPI backend for LangGraph + Gemini RAG assistant",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # We can change this with frotnend url in prod
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(router)

# #Start ngrok tunnel
# public_url = ngrok.connect(8000, authtoken_from_env=True)
# print(f"Public ngrok URL: {public_url}")
