from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from src.intelligence import analyze_message
from src.retriever import retrieve_documents
from src.response_generator import (
    FALLBACK_RESPONSE,
    OUT_OF_SCOPE_RESPONSE,
    UNCLEAR_SCOPE_RESPONSE,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent
STATIC_DIR = PROJECT_ROOT / "src" / "static"
INDEX_FILE = STATIC_DIR / "index.html"


app = FastAPI(
    title="AWN AI API",
    description="AI-powered customer support intelligence",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static"
)


class ChatRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=2000
    )


class ChatResponse(BaseModel):
    message: str
    scope: str
    category: str | None
    intent: str | None
    response: str
    sources: list[dict]


@app.api_route("/", methods=["GET", "HEAD"])
def root(request: Request):
    html_content = INDEX_FILE.read_text(encoding="utf-8")
    if request.method == "HEAD":
        return Response(status_code=200, media_type="text/html", headers={"Content-Length": str(len(html_content.encode("utf-8")))})
    return HTMLResponse(content=html_content)


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    message = request.message.strip()

    if not message:
        raise HTTPException(
            status_code=422,
            detail="Message cannot be empty."
        )

    # Step 1: Analyze message scope
    analysis = analyze_message(message)

    scope = analysis["scope"]

    # Step 2: Handle messages outside the service scope
    if scope == "OUT_OF_SCOPE":
        return {
            "message": message,
            "scope": scope,
            "category": None,
            "intent": None,
            "response": OUT_OF_SCOPE_RESPONSE,
            "sources": []
        }

    # Step 3: Ask for clarification when scope is unclear
    if scope == "UNCLEAR_SCOPE":
        return {
            "message": message,
            "scope": scope,
            "category": None,
            "intent": None,
            "response": UNCLEAR_SCOPE_RESPONSE,
            "sources": []
        }

    # Step 4: Retrieve relevant knowledge
    documents = retrieve_documents(
        query=message,
        top_k=3,
        intent=analysis["intent"]
    )

    # Step 5: Build response from retrieved knowledge
    if documents:
        response = (
            "I found the following information "
            "in our knowledge base:\n\n"
            + documents[0]["content"]
        )
    else:
        response = FALLBACK_RESPONSE

    return {
        "message": message,
        "scope": scope,
        "category": analysis["category"],
        "intent": analysis["intent"],
        "response": response,
        "sources": documents
    }