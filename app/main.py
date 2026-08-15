import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from app.rag_engine import RAGEngine

# ── Create app and load RAG engine ────────────────────────────────────────────
# RAGEngine loads once at startup — not on every request
# This is important for performance — building the index takes time
print("Starting up — loading RAG engine...")
rag_engine = RAGEngine()
print("RAG engine ready.")

app = FastAPI(
    title="Customer Support Chatbot API",
    description="RAG-powered customer support chatbot — answers grounded in company knowledge base",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Schemas ───────────────────────────────────────────────────────────────────
class QuestionRequest(BaseModel):
    question: str

class Source(BaseModel):
    title: str
    category: str
    relevance_score: float

class ChatResponse(BaseModel):
    question: str
    answer: str
    sources: List[Source]
    confidence: str
    confidence_score: float
    disclaimer: str

# ── Endpoints ─────────────────────────────────────────────────────────────────
@app.get("/")
def root():
    return {
        "message": "Customer Support Chatbot API is running",
        "docs": "/docs",
        "endpoints": ["/ask", "/health", "/topics"]
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "documents_indexed": len(rag_engine.documents),
        "approach": "TF-IDF RAG — retrieval grounded, no hallucination"
    }

@app.get("/topics")
def get_topics():
    """Returns all topics the chatbot can answer questions about"""
    categories = list(set(
        doc["category"] for doc in rag_engine.documents
    ))
    return {
        "topics": categories,
        "total_documents": len(rag_engine.documents)
    }

@app.post("/ask", response_model=ChatResponse)
def ask_question(request: QuestionRequest):
    """
    Main chat endpoint.
    Receives a question, retrieves relevant knowledge base documents,
    and returns a grounded answer with source attribution.
    
    Every answer shows which document it came from — no hallucination possible
    because we only return content that exists in our knowledge base.
    """
    # Validate input
    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    if len(request.question) > 500:
        raise HTTPException(
            status_code=400,
            detail="Question too long — maximum 500 characters"
        )

    # Run RAG pipeline
    result = rag_engine.ask(request.question)

    # Build source list
    sources = [
        Source(
            title=s["title"],
            category=s["category"],
            relevance_score=s["relevance_score"]
        )
        for s in result["sources"]
    ]

    return ChatResponse(
        question=result["query"],
        answer=result["answer"],
        sources=sources,
        confidence=result["confidence"],
        confidence_score=result["confidence_score"],
        disclaimer="Answers are grounded in our knowledge base. For complex issues please contact support directly."
    )