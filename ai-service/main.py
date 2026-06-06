import os
import tempfile
from typing import Dict
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
import httpx
from dotenv import load_dotenv
from rag_pipeline import initialize_pipeline

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="AI Document Q&A Service", version="1.0.0")

# Global variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Process uploaded document through RAG pipeline.
    """
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{file.filename}") as tmp_file:
        content = await file.read()
        tmp_file.write(content)
        tmp_file_path = tmp_file.name

    try:
        # Initialize and process document through RAG pipeline
        pipeline = initialize_pipeline()
        success = pipeline.process_document(tmp_file_path)

        if not success:
            raise HTTPException(status_code=500, detail="Failed to process document")

        return JSONResponse(
            status_code=200,
            content={"status": "success", "message": "File processed and stored in vector database"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up temporary file
        if os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)

@app.post("/ask")
async def ask_question(request: Dict[str, str]):
    """
    Answer question using RAG pipeline and OpenRouter LLM.
    """
    if not OPENROUTER_API_KEY:
        raise HTTPException(status_code=500, detail="OPENROUTER_API_KEY not configured")

    question = request.get("question", "").strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question is required")

    try:
        # Initialize pipeline
        pipeline = initialize_pipeline()

        # Get relevant context for the question
        context = pipeline.get_context_for_query(question, k=3)

        if not context:
            return JSONResponse(
                status_code=200,
                content={"answer": "I couldn't find relevant information in the document to answer your question."}
            )

        # Prepare prompt for OpenRouter
        system_prompt = """You are a helpful AI assistant that answers questions based on the provided context.
        Use only the information from the context to answer the question. If the context doesn't contain
        enough information to answer the question, say so clearly. Be concise and accurate."""

        user_prompt = f"""Context:
{context}

Question: {question}

Answer:"""

        # Call OpenRouter API with increased timeout for large documents
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                OPENROUTER_URL,
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "openai/gpt-oss-120b:free",  # Using a free model available on OpenRouter
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "max_tokens": 500,
                    "temperature": 0.7
                }
            )

            if response.status_code != 200:
                print(f"OpenRouter Error Response: {response.text}")
                raise HTTPException(status_code=response.status_code, detail=f"OpenRouter API failed: {response.text}")

            result = response.json()
            answer = result.get("choices", [{}])[0].get("message", {}).get("content", "No answer generated")

            return JSONResponse(
                status_code=200,
                content={"answer": answer.strip()}
            )

    except Exception as e:
        print(f"Error in ask_question: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)