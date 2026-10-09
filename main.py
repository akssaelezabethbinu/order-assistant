
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from agent import ask_order_assistant

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="Order Assistant")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1000)


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/")
def home():
    index_file = STATIC_DIR / "index.html"
    return FileResponse(index_file)


@app.post("/api/chat")
def chat(request: ChatRequest):
    try:
        answer = ask_order_assistant(request.question)
        return {"answer": answer}
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Unable to process your question. Please try again."
        ) from exc