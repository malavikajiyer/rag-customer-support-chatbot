import pytest
from fastapi.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["documents_indexed"] == 8

def test_topics_endpoint():
    response = client.get("/topics")
    assert response.status_code == 200
    assert "topics" in response.json()

def test_ask_pricing_question():
    response = client.post("/ask", json={"question": "How much does the professional plan cost?"})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sources" in data
    assert "confidence" in data
    assert len(data["sources"]) > 0

def test_ask_returns_correct_fields():
    response = client.post("/ask", json={"question": "How do I reset my password?"})
    assert response.status_code == 200
    data = response.json()
    assert "question" in data
    assert "answer" in data
    assert "confidence_score" in data
    assert "disclaimer" in data

def test_empty_question_returns_400():
    response = client.post("/ask", json={"question": ""})
    assert response.status_code == 400

def test_long_question_returns_400():
    response = client.post("/ask", json={"question": "x" * 501})
    assert response.status_code == 400