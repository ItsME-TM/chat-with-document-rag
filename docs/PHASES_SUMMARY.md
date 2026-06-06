# Cross-RAG Hub - Phased Implementation Plan

This document summarizes the three-phase approach to building the AI-powered document Q&A system using OpenRouter's free gpy-oss-120b:free model.

## Phase 1: Working Skeleton
**Goal**: Create a minimal end-to-end skeleton demonstrating basic architecture and communication.

**Key Deliverables**:
- Python AI service with FastAPI endpoints returning fixed responses
- .NET API service with controllers returning fixed responses  
- Frontend HTML page with basic upload/question UI
- Repository structure matching the project plan
- Services communicating with skeleton/fixed responses

**Files**: `docs/phase1.md`

## Phase 2: Core RAG Pipeline Implementation
**Goal**: Implement the full RAG pipeline in Python service and connect .NET API to it.

**Key Deliverables**:
- Python service with complete RAG pipeline (document loading, chunking, embeddings, FAISS, OpenRouter LLM)
- .NET API service properly forwarding requests to Python service
- Environment configuration for API keys
- End-to-end testing: upload document → ask question → get meaningful answer

**Files**: `docs/phase2.md`

## Phase 3: Frontend, Polish & Documentation
**Goal**: Complete frontend UI, integrate all components, add polish, and create comprehensive documentation.

**Key Deliverables**:
- Fully functional frontend UI with upload/chat interface
- Complete end-to-end integration (Frontend → .NET → Python → OpenRouter → Answer)
- Polish: loading states, error handling, responsive design
- Comprehensive README with setup, usage, and troubleshooting instructions
- Ready for demonstration matching the project plan demo script

**Files**: `docs/phase3.md`

## Overall Success Criteria
By completing all three phases, you will have:
1. A working full-stack AI document Q&A system
2. Zero-cost LLM usage via OpenRouter gpy-oss-120b:free
3. Demonstrated proficiency in Python (.NET, FastAPI, LangChain, FAISS)
4. Demonstrated proficiency in .NET (ASP.NET Core, HTTP clients, dependency injection)
5. Demonstrated proficiency in frontend development (HTML, JavaScript)
6. Clear documentation enabling others to run and understand the project
7. Presentation-ready code for interviews or demonstrations

## Repository Structure
```
cross-rag-hub/
├─ ai-service/
│  ├─ main.py                # FastAPI endpoints (/upload, /ask)
│  ├─ rag_pipeline.py        # Loading, chunking, embedding, retrieval
│  ├─ requirements.txt
│  └─ .env                   # OPENAI_API_KEY (not committed)
├─ dotnet-api/
│  ├─ Controllers/
│  │   └─ DocumentController.cs   # /api/upload, /api/ask
│  ├─ Services/
│  │   └─ AiService.cs            # HttpClient wrapper
│  └─ Program.cs
├─ frontend/
│  └─ index.html                # Upload + chat UI
└─ README.md                    # Setup & run instructions
```

Each phase builds upon the previous one, allowing for incremental development and testing.