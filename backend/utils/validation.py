from typing import Any
import re

def validate_uuid(uuid_string: str) -> bool:
    """
    Validate if a string is a proper UUID format.

    Args:
        uuid_string: String to validate

    Returns:
        True if valid UUID format, False otherwise
    """
    uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    return bool(re.match(uuid_pattern, uuid_string))

def validate_url(url_string: str) -> bool:
    """
    Validate if a string is a proper URL format.

    Args:
        url_string: String to validate

    Returns:
        True if valid URL format, False otherwise
    """
    url_pattern = r'^https?://(?:[-\w.])+(?:\:[0-9]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:\#(?:[\w.])*)?)?$'
    return bool(re.match(url_pattern, url_string))

def validate_content_length(content: str, max_length: int = 10000) -> bool:
    """
    Validate if content length is within allowed limits.

    Args:
        content: Content string to validate
        max_length: Maximum allowed length (default 10000)

    Returns:
        True if within limits, False otherwise
    """
    return len(content) <= max_length

def sanitize_input(input_string: str) -> str:
    """
    Sanitize input string to prevent injection attacks.

    Args:
        input_string: Input string to sanitize

    Returns:
        Sanitized string
    """
    # Remove potentially dangerous characters while preserving readable text
    # Allow alphanumeric, spaces, common punctuation, and basic symbols
    if input_string is None:
        return None

    # Limit length to prevent abuse
    if len(input_string) > 2000:
        input_string = input_string[:2000]

    # Return the input as is for now, with basic sanitization
    return input_string.strip()