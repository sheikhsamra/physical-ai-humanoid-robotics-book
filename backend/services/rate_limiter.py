"""
Rate Limiting Service

This module provides rate limiting functionality for API endpoints.
"""
import time
from collections import defaultdict, deque
from typing import Dict, Optional
from threading import Lock

class SimpleRateLimiter:
    """
    A simple rate limiter that tracks requests per IP or user.
    """

    def __init__(self, max_requests: int = 10, window_size: int = 60):
        """
        Initialize the rate limiter.

        Args:
            max_requests: Maximum number of requests allowed per window
            window_size: Time window in seconds
        """
        self.max_requests = max_requests
        self.window_size = window_size
        self.requests: Dict[str, deque] = defaultdict(deque)
        self.lock = Lock()

    def is_allowed(self, identifier: str) -> bool:
        """
        Check if a request from the given identifier is allowed.

        Args:
            identifier: A unique identifier (e.g., IP address, user ID)

        Returns:
            True if the request is allowed, False otherwise
        """
        with self.lock:
            current_time = time.time()
            # Remove old requests outside the time window
            while (self.requests[identifier] and
                   current_time - self.requests[identifier][0] > self.window_size):
                self.requests[identifier].popleft()

            # Check if we've exceeded the limit
            if len(self.requests[identifier]) >= self.max_requests:
                return False

            # Add the current request
            self.requests[identifier].append(current_time)
            return True

    def get_reset_time(self, identifier: str) -> Optional[float]:
        """
        Get the time when the rate limit will reset for the identifier.

        Args:
            identifier: A unique identifier (e.g., IP address, user ID)

        Returns:
            The time when the rate limit will reset, or None if not limited
        """
        with self.lock:
            if identifier in self.requests and len(self.requests[identifier]) > 0:
                oldest_request = self.requests[identifier][0]
                return oldest_request + self.window_size
            return None


# Global rate limiter instance
rate_limiter = SimpleRateLimiter(max_requests=10, window_size=60)  # 10 requests per minute