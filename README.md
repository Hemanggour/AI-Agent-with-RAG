# AI Agent with RAG pipeline

An AI-powered document Q&A assistant enriched with a Retrieval-Augmented Generation (RAG) pipeline. This project leverages Google Gemini LLM and custom document embeddings to provide accurate, context-aware answers from your own PDF files. Easily run locally or share online via ngrok.

---

## Features

- **Conversational Q&A:** Ask questions about your documents and get AI-powered answers.
- **RAG Pipeline:** Combines LLM with document retrieval for more accurate responses.
- **Custom Document Support:** Index your own PDFs for personalized knowledge.
- **Streamlit Frontend:** Simple, interactive web UI.
- **FastAPI Backend:** Robust, scalable API.
- **Easy Online Sharing:** Serve your assistant online using ngrok.
- **One-Command Launch:** Start everything with a single script.

---

## Prerequisites

- **Python:** 3.10 or higher
- **pip:** Python package manager

---

## Setup Instructions

### 1. Clone the Repository

```sh
git clone https://github.com/Hemanggour/AI-Agent-with-RAG.git
cd AI-Agent-with-RAG
```

### 2. Install Dependencies

```sh
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the project root (or edit the existing one):

```env
GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY"
NGROK_AUTHTOKEN = "YOUR_NGROK_AUTHTOKEN"
```

- **Google API Key:** Get from [Google AI Studio](https://aistudio.google.com/app/apikey)
- **ngrok Auth Token:** Get from [ngrok dashboard](https://dashboard.ngrok.com/get-started/your-authtoken)

---

### 4. Add Your PDF Documents

- Place your PDF(s) in the `data/` directory.
- By default, the project uses `Indian-Accounting-Standards-IND-AS.pdf`.
- To use your own PDF, update the `doc_path` variable in `backend/populate_db.py` with your file name.

---

### 5. Populate the Vector Database

**This step is required before first use or after adding new PDFs.**

```sh
python backend/populate_db.py
```

---

## Running the Project

### Option 1: Local Mode (Frontend + Backend)

Runs everything locally (Streamlit UI at `http://localhost:8501`):

```sh
python launch.py
```

---

### Option 2: Online Mode (via ngrok)

Share your assistant online (ngrok public URL will be shown in the terminal):

```sh
python launch.py --online
```

---

### Option 3: Manual Mode

- **Backend only:**  
  ```sh
  uvicorn backend.main:app --reload
  ```
- **Frontend only (local):**  
  ```sh
  streamlit run frontend/app.py
  ```
- **Frontend only (ngrok):**  
  ```sh
  python frontend/serve.py
  ```

---

## API Usage

- **Endpoint:** `/chat`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "message": "YOUR QUESTION HERE"
  }
  ```
- **Response:**  
  ```json
  {
    "response": "AGENT_RESPONSE"
  }
  ```

---

## Running Tests

To verify your setup, run:

```sh
python test_run.py
```

---

## Notes

- **ngrok:**  
  No manual installation needed; `pyngrok` handles everything. Just set your `NGROK_AUTHTOKEN` in `.env`.
- **Multiple PDFs:**  
  You can add multiple PDFs to `data/` and update `doc_path` in `populate_db.py` as needed.
- **First Run:**  
  Always run `populate_db.py` after adding or changing PDFs.

---

## Project Structure

```
AI-Agent-with-RAG/
│
├── backend/
│   ├── main.py            # FastAPI backend
│   ├── api/               # API routes
│   ├── populate_db.py     # Script to index PDFs
│   └── ...
├── frontend/
│   ├── app.py             # Streamlit frontend
│   ├── serve.py           # ngrok serving script
│   └── ...
├── data/                  # Place your PDFs here
├── vectorstore/           # Vector DB files (auto-generated)
├── launch.py              # One-command launcher
├── test_run.py            # Test script
├── requirements.txt
├── .env
└── README.md
```

---

## License

MIT License.

---

## Credits

Built with FastAPI, Streamlit, Google Gemini, and LangChain / LangGraph.

---

**Enjoy your AI-powered document**