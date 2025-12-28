from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import field_serializer

class ErrorResponse(BaseModel):
    """
    Represents an error response when the API encounters an issue processing a query.
    """
    error: str = Field(..., description="Human-readable error message")
    code: str = Field(..., description="Machine-readable error code")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.now, description="When the error occurred")

    @field_serializer('timestamp')
    def serialize_timestamp(self, dt: datetime) -> str:
        return dt.isoformat()

    def model_post_init(self, __context):
        """Validate that error fields are properly set after initialization."""
        if not self.error or not self.error.strip():
            raise ValueError('Error message must be non-empty')

        if not self.code or not self.code.strip():
            raise ValueError('Error code must be non-empty')