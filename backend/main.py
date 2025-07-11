from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router

# 👇 Ngrok import
from pyngrok import ngrok

app = FastAPI(
    title="Accounting AI Assistant",
    description="FastAPI backend for LangGraph + Gemini RAG assistant",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific frontend in prod
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(router)

# # 👇 Start ngrok tunnel
# public_url = ngrok.connect(8000)
# print(f"🔗 Public ngrok URL: {public_url}")
