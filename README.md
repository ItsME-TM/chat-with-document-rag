# AI Document Q&A System - Phase 1: Working Skeleton

This is the Phase 1 implementation of the AI Document Q&A system. It provides a minimal end-to-end skeleton that demonstrates the architecture and basic communication between the frontend, .NET API, and Python AI service.

## Project Structure

```
cross-rag-hub/
├── ai-service/          # Python FastAPI service (skeleton)
│   ├── main.py
│   └── requirements.txt
├── dotnet-api/          # ASP.NET Core Web API (skeleton)
│   ├── Program.cs
│   ├── Controllers/
│   │   └─ DocumentController.cs
│   └── Services/
│       └─ AiService.cs
└── frontend/            # Simple HTML/JavaScript frontend
    └── index.html
```

## Prerequisites

- Python 3.8+
- .NET 8.0 SDK
- A modern web browser

## Setup and Running

### 1. Python AI Service

Navigate to the `ai-service` directory and install dependencies:

```bash
cd ai-service
pip install -r requirements.txt
```

Run the service:

```bash
uvicorn main:app --reload
```

The service will be available at `http://localhost:8000`.

### 2. .NET API Service

Navigate to the `dotnet-api` directory and run:

```bash
cd dotnet-api
dotnet run
```

The service will be available at `http://localhost:5000` (or another port if 5000 is in use).

### 3. Frontend

Open `frontend/index.html` in a web browser. The frontend is configured to call the .NET API at `/api/upload` and `/api/ask` (relative to the frontend's origin).

**Note**: For the frontend to work correctly, you need to serve it from a web server (to avoid CORS issues). You can use a simple Python HTTP server:

```bash
cd frontend
python -m http.server 3000
```

Then open your browser to `http://localhost:3000`.

## Expected Behavior

- **Upload**: Select a file (any type) and click "Upload". You should see a success message: "Upload successful: File received".
- **Ask**: Type a question in the input box and click "Ask". You should see the answer: "This is a skeleton response.".

## Next Steps (Phase 2)

In Phase 2, we will implement the full RAG pipeline in the Python service:
- Process uploaded documents (PDF, DOCX, TXT) using LangChain loaders.
- Split text into chunks and generate embeddings using OpenAI's `text-embedding-3-small`.
- Store vectors in FAISS for fast similarity search.
- Use the OpenRouter free model `gpy-oss-120b:free` to generate answers based on retrieved context.
- The .NET API will forward requests to the Python service and return the actual results.

## Troubleshooting

- **Frontend cannot connect to .NET API**: Ensure the .NET API is running and that the frontend is served from a server (not opened directly as a file) to avoid CORS issues.
- **Port conflicts**: If the default ports (8000 for Python, 5000 for .NET) are in use, you can change them in the respective service configurations.
- **Dependencies**: Make sure you have installed all required dependencies for each service.

## License

This project is for educational and demonstration purposes.