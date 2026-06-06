# Phase 1: Working Skeleton

## Goal
Create a minimal end-to-end skeleton that demonstrates the architecture and basic communication between components without implementing the full RAG pipeline.

## Components

### AI Service (Python)
- Create `ai-service/` directory
- `main.py`: FastAPI app with two endpoints:
  - `POST /upload`: Returns fixed JSON `{"status": "success", "message": "File received"}`
  - `POST /ask`: Returns fixed JSON `{"answer": "This is a skeleton response."}`
- `requirements.txt`: List `fastapi`, `uvicorn`
- `.env.example`: Placeholder for `OPENAI_API_KEY` (not committed)

### .NET API Service
- Create `dotnet-api/` directory
- ASP.NET Core 8 Web API project
- `Controllers/DocumentController.cs`:
  - `POST /api/upload`: Returns fixed JSON (or calls Python skeleton endpoint)
  - `POST /api/ask`: Returns fixed JSON (or calls Python skeleton endpoint)
- `Services/AiService.cs`: Stub implementation returning fixed responses
- `Program.cs`: Basic ASP.NET Core setup

### Frontend
- Create `frontend/` directory
- `index.html`: Simple HTML page with:
  - File input for document upload
  - Text input for questions
  - Button to send question
  - Area to display answer
  - JavaScript to call .NET API endpoints (which return skeleton responses)

## Communication Flow
Frontend → .NET API → Python Service (all returning fixed/skeleton responses)

## Success Criteria
- All three services can be started independently
- Frontend can upload a file and receive a response from .NET API
- .NET API can forward requests to Python service and receive responses
- Basic project structure matches the repository plan

## Deliverables
- Repository structure as outlined in Section 4 of the project plan
- Skeleton implementations in each service
- Basic README with instructions to run each service separately