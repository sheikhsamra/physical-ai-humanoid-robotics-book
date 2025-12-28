# RAG Chatbot API Documentation

## Overview

The RAG Chatbot API provides an interface to interact with the Physical AI and Humanoid Robotics book through an intelligent agent. The API accepts user queries and returns contextually relevant responses based on the book content.

## Base URL

```
http://localhost:8000
```

## Endpoints

### POST /chat

Send a query to the RAG agent and receive a response.

#### Request

**Content-Type:** `application/json`

**Body:**
```json
{
  "query": "string (required)",
  "sessionId": "string (optional, UUID format)"
}
```

**Parameters:**
- `query`: The user's question or input text (max 2000 characters)
- `sessionId`: Optional identifier for conversation tracking (UUID format)

#### Response

**Success Response (200):**
```json
{
  "content": "string",
  "sources": [
    {
      "id": "string",
      "content": "string",
      "source_url": "string",
      "module": "string",
      "section": "string",
      "score": "number"
    }
  ],
  "query": "string",
  "agentId": "string",
  "timestamp": "string (ISO 8601 format)"
}
```

**Error Response (400, 429, 500):**
```json
{
  "error": "string",
  "code": "string",
  "details": "object (optional)",
  "timestamp": "string (ISO 8601 format)"
}
```

#### Example Request

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is Physical AI?",
    "sessionId": "123e4567-e89b-12d3-a456-426614174000"
  }'
```

#### Example Response

```json
{
  "content": "Physical AI represents a paradigm shift toward intelligence that is embodied in physical systems...",
  "sources": [
    {
      "id": "doc-001",
      "content": "Physical AI represents a paradigm shift...",
      "source_url": "https://example.com/book/physical-ai",
      "module": "introduction",
      "section": "definition",
      "score": 0.87
    }
  ],
  "query": "What is Physical AI?",
  "agentId": "rag-agent-1",
  "timestamp": "2025-12-27T10:00:00"
}
```

### GET /health

Check the health status of the API.

#### Response

**Success Response (200):**
```json
{
  "status": "healthy"
}
```

### GET /

Get the root endpoint status.

#### Response

**Success Response (200):**
```json
{
  "message": "RAG Chatbot API is running!"
}
```

## Error Codes

- `EMPTY_QUERY`: The query field is empty
- `RATE_LIMIT_EXCEEDED`: Too many requests from the same IP
- `PROCESSING_ERROR`: An error occurred while processing the query
- `QUERY_TOO_LONG`: The query exceeds the maximum length

## Rate Limiting

The API implements rate limiting to prevent abuse. The current limit is 10 requests per minute per IP address.

## CORS Policy

The API allows requests from:
- `http://localhost:3000`
- `http://localhost:3001`
- `http://localhost:8000`
- `http://localhost:3002`

## Testing the API

You can test the API using curl or any HTTP client:

```bash
# Test the chat endpoint
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the main components of a humanoid robot?"}'

# Test the health endpoint
curl http://localhost:8000/health
```