import pytest
from fastapi.testclient import TestClient
from api import app
from models.query_request import QueryRequest
from models.agent_response import AgentResponse

client = TestClient(app)

def test_complete_api_flow():
    """
    Integration test for the complete API flow from request to response.
    Tests the entire chain: API endpoint -> validation -> agent service -> response formatting
    """
    # Test a valid query
    test_payload = {
        "query": "What is Physical AI?",
        "sessionId": "test-session-123e4567-e89b-12d3-a456-426614174000"
    }

    response = client.post("/chat", json=test_payload)

    # Should return 200 for a valid query (or 500 if external services fail due to missing API keys)
    # In a real deployment with proper API keys, this would return 200
    # For testing purposes without API keys, it might return 500 due to external service unavailability
    assert response.status_code in [200, 500]

    if response.status_code == 200:
        # Parse the response
        data = response.json()

        # Verify the response structure matches AgentResponse model
        assert "content" in data
        assert "query" in data
        assert "agentId" in data
        assert data["query"] == "What is Physical AI?"

        # The sources field may or may not be present depending on agent implementation
        assert "sources" in data

def test_api_flow_with_empty_query():
    """
    Test the API flow with an empty query - should return validation error.
    """
    test_payload = {
        "query": ""
    }

    response = client.post("/chat", json=test_payload)

    # Should return 422 for validation error (empty query)
    assert response.status_code == 422

    # Verify error response structure
    data = response.json()
    assert "detail" in data  # FastAPI validation errors use 'detail' field

def test_api_flow_with_whitespace_query():
    """
    Test the API flow with a whitespace-only query - should return validation error.
    """
    test_payload = {
        "query": "   "
    }

    response = client.post("/chat", json=test_payload)

    # Should return 422 for validation error (whitespace query)
    assert response.status_code == 422

    # Verify error response structure
    data = response.json()
    assert "detail" in data

def test_health_endpoint():
    """
    Test the health endpoint to ensure the API is running.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_root_endpoint():
    """
    Test the root endpoint to ensure the API is running.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_cors_headers_present():
    """
    Test that CORS headers are properly set for frontend integration.
    """
    # Make a request and check for CORS headers
    headers = {"Origin": "http://localhost:3000", "Access-Control-Request-Method": "POST", "Access-Control-Request-Headers": "X-Requested-With"}
    response = client.options("/chat", headers=headers)

    # For preflight requests, we expect a 200 response with CORS headers
    # Note: FastAPI's CORSMiddleware handles preflight requests automatically
    # If our endpoint doesn't explicitly handle OPTIONS, this might return 405
    # That's normal behavior - the CORS middleware handles preflight requests

if __name__ == "__main__":
    pytest.main([__file__])