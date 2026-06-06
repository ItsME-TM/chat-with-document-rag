from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI(title="AI Document Q&A Service", version="1.0.0")

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Skeleton endpoint for file upload.
    In Phase 2, this will process the document through the RAG pipeline.
    """
    return JSONResponse(
        status_code=200,
        content={"status": "success", "message": "File received"}
    )

@app.post("/ask")
async def ask_question(question: dict):
    """
    Skeleton endpoint for asking questions.
    In Phase 2, this will use the RAG pipeline to generate answers.
    """
    return JSONResponse(
        status_code=200,
        content={"answer": "This is a skeleton response."}
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)