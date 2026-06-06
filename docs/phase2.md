# Phase 2: Core RAG Pipeline Implementation

## Goal
Implement the full RAG pipeline in the Python AI service and connect the .NET API to it, enabling document upload and question answering with the OpenRouter free model.

## Components

### AI Service (Python) - Full Implementation
- `main.py`: 
  - `POST /upload`: 
    - Accepts file upload (PDF, DOCX, TXT)
    - Saves file temporarily
    - Processes document through RAG pipeline (load, chunk, embed, store in FAISS)
    - Returns document ID or status
  - `POST /ask`:
    - Accepts question and document ID (or uses latest)
    - Embeds question, retrieves top-k chunks from FAISS
    - Builds prompt with retrieved context and question
    - Calls OpenRouter `gpy‑oss‑120b:free` via HTTP
    - Returns answer and optionally source chunks
- `rag_pipeline.py`: 
  - Contains the core RAG logic:
    - Document loading (using `pypdf`, `python-docx`)
    - Text splitting (`RecursiveCharacterTextSplitter`)
    - Embedding generation (OpenAI `text-embedding-3-small`)
    - FAISS vector store management
    - Query processing and retrieval
- `requirements.txt`: 
  - `fastapi`, `uvicorn`, `langchain`, `faiss-cpu`, `openai`, `httpx`, `pypdf`, `python-docx`, `python-multipart`
- `.env`: 
  - `OPENAI_API_KEY` (for embeddings)
  - `OPENROUTER_API_KEY` (for LLM access)

### .NET API Service
- `Controllers/DocumentController.cs`:
  - `POST /api/upload`: 
    - Receives file, forwards to Python `/upload` endpoint
    - Returns response from Python service
  - `POST /api/ask`:
    - Receives question, forwards to Python `/ask` endpoint
    - Returns answer from Python service
- `Services/AiService.cs`:
  - Implements HTTP client calls to Python service
  - Handles serialization/deserialization
- `Program.cs`: 
  - Configure HTTP client for AiService
  - Enable CORS for frontend
  - Swagger setup

## Communication Flow
Frontend (later) → .NET API → Python Service (RAG pipeline) → OpenRouter LLM → Answer

## Success Criteria
- Python service can process a document and store vectors in FAISS
- Python service can answer questions based on the document using RAG
- .NET API successfully forwards requests to Python service and returns responses
- Both services run without errors
- End-to-end test: upload a document, ask a question, get a meaningful answer

## Deliverables
- Fully functional Python AI service with RAG pipeline
- .NET API service that correctly proxies to Python service
- Updated README with instructions to run both services and test the RAG flow
- Example document and test questions for verification