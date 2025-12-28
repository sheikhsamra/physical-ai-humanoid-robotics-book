from pydantic import BaseModel, Field
from typing import Optional
import re
from pydantic import field_validator

class QueryRequest(BaseModel):
    """
    Represents a user's query sent to the RAG agent through the API.
    """
    query: str = Field(..., description="The user's question or input text", max_length=2000)
    sessionId: Optional[str] = Field(None, description="Identifier for conversation tracking")

    @field_validator('query')
    @classmethod
    def validate_query(cls, v):
        if not v or not v.strip():
            raise ValueError('Query must be non-empty')
        if not re.match(r'^[\w\s\.\,\!\?\;\:\-\(\)\[\]\{\}\'\"\/\+\=\*\&\%\#\@\~\`\|\<\>]+$', v):
            # Allow basic printable characters but reject potentially harmful ones
            raise ValueError('Query contains invalid characters')
        return v.strip()

    @field_validator('sessionId', mode='before')
    @classmethod
    def validate_session_id(cls, v):
        if v is None:
            return v
        # Basic UUID format validation (8-4-4-4-12 hex characters)
        uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        if not re.match(uuid_pattern, v):
            raise ValueError('sessionId must follow UUID format')
        return v