from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class Source(BaseModel):
    """
    Represents a source document used in generating the agent's response.
    """
    id: str = Field(..., description="Unique identifier for the source")
    content: str = Field(..., description="The content of the source", max_length=10000)
    source_url: str = Field(..., description="URL where the source can be found")
    module: str = Field(..., description="Module or section of the book this source belongs to")
    section: str = Field(..., description="Specific section within the module")
    score: float = Field(..., description="Relevance score (0.0 to 1.0)", ge=0.0, le=1.0)

    def model_post_init(self, __context):
        """Validate that source fields are properly set after initialization."""
        if not self.id or not self.id.strip():
            raise ValueError('Source ID must be non-empty')

        if not self.content or not self.content.strip():
            raise ValueError('Source content must be non-empty')

        if not self.module or not self.module.strip():
            raise ValueError('Module must be non-empty')

        if not self.section or not self.section.strip():
            raise ValueError('Section must be non-empty')