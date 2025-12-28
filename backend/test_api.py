import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "RAG Chatbot API is running!"}

def test_health_endpoint():
    """Test the health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_chat_endpoint_with_valid_query():
    """Test the chat endpoint with a valid query"""
    test_payload = {
        "query": "What is Physical AI?"
    }
    response = client.post("/chat", json=test_payload)
    assert response.status_code == 200

    data = response.json()
    assert "content" in data
    assert "query" in data
    assert data["query"] == "What is Physical AI?"
    assert "agentId" in data

def test_chat_endpoint_with_empty_query():
    """Test the chat endpoint with an empty query - should return 422 validation error"""
    test_payload = {
        "query": ""
    }
    response = client.post("/chat", json=test_payload)
    assert response.status_code == 422

    data = response.json()
    assert "detail" in data  # FastAPI validation errors use 'detail' field

def test_chat_endpoint_with_whitespace_query():
    """Test the chat endpoint with a whitespace-only query - should return 422 validation error"""
    test_payload = {
        "query": "   "
    }
    response = client.post("/chat", json=test_payload)
    assert response.status_code == 422

    data = response.json()
    assert "detail" in data  # FastAPI validation errors use 'detail' field

if __name__ == "__main__":
    pytest.main([__file__])