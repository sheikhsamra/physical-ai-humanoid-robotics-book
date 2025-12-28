# Physical AI and Humanoid Robotics Book

## Table of Contents
- [Overview](#overview)
- [Backend Setup](#backend-setup)
- [Frontend Setup](#frontend-setup)
- [Deployment](#deployment)
- [API Documentation](#api-documentation)
- [Development](#development)

## Overview

This repository contains the Physical AI and Humanoid Robotics book with an integrated RAG chatbot. The system consists of:

- A Docusaurus-based frontend for the book
- A FastAPI backend with RAG agent integration
- A chatbot UI component for interacting with the book content

## Backend Setup

### Prerequisites

- Python 3.8+
- Access to Qdrant vector database
- Cohere API key
- Groq API key

### Installation

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip install fastapi uvicorn python-dotenv openai-agents groq cohere qdrant-client
   ```

3. Set up environment variables:
   Create a `.env` file with the following variables:
   ```env
   GROQ_API_KEY=your_groq_api_key
   COHERE_API_KEY=your_cohere_api_key
   QDRANT_HOST=your_qdrant_host
   QDRANT_API_KEY=your_qdrant_api_key
   QDRANT_PORT=6333
   QDRANT_COLLECTION_NAME=docusaurus_content
   GROQ_MODEL=llama-3.1-8b-instant
   ```

4. Run the backend server:
   ```bash
   uvicorn api:app --reload --port 8000
   ```

The backend server will be available at `http://localhost:8000`.

## Frontend Setup

### Prerequisites

- Node.js 16+
- npm or yarn

### Installation

1. Navigate to the my-book directory:
   ```bash
   cd my-book
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run start
   ```

The frontend will be available at `http://localhost:3000`.

## Deployment

### Backend Deployment

For production deployment of the backend:

1. **Environment Configuration**:
   - Set up environment variables for production
   - Use secure methods to store API keys (environment variables, secrets management)

2. **Production Server**:
   - Use a production ASGI server like Gunicorn:
     ```bash
     pip install gunicorn
     gunicorn backend.api:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
     ```

3. **Performance Optimization**:
   - Implement Redis for caching
   - Set up proper logging and monitoring
   - Configure rate limiting appropriately

4. **Security**:
   - Update CORS settings for production domains
   - Implement proper authentication if needed
   - Secure API endpoints

### Frontend Deployment

The Docusaurus frontend can be deployed:

1. **Build the static site**:
   ```bash
   npm run build
   ```

2. **Serve the static files**:
   - Deploy the `build/` directory to a static hosting service
   - Configure your web server to serve the static files

### Docker Deployment (Optional)

You can containerize the application:

**Backend Dockerfile**:
```Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .

EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Frontend Dockerfile**:
```Dockerfile
FROM node:16

WORKDIR /app

COPY my-book/package*.json ./
RUN npm install

COPY my-book/ .

EXPOSE 3000

CMD ["npm", "run", "start"]
```

## API Documentation

The backend API provides the following endpoints:

- `POST /chat`: Process user queries with the RAG agent
- `GET /health`: Check API health status
- `GET /`: API status

For detailed API documentation, visit the API after starting the server: `http://localhost:8000/docs`

## Development

### Running Tests

Backend tests:
```bash
cd backend
python -m pytest
```

### Project Structure

```
backend/
├── api.py              # FastAPI application
├── agent.py            # RAG agent implementation
├── models/             # Pydantic models
├── services/           # Service layer
├── utils/              # Utility functions
└── docs/               # Documentation
my-book/
├── src/
│   └── components/     # React components (including Chatbot)
└── docs/               # Book content
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request
