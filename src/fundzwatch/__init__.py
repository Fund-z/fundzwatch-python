"""FundzWatch.ai Python SDK - Real-time business event intelligence for AI agents."""

from fundzwatch.client import FundzWatch
from fundzwatch.exceptions import (
    FundzWatchError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
    APIError,
)

__version__ = "1.0.0"
__all__ = [
    "FundzWatch",
    "FundzWatchError",
    "AuthenticationError",
    "RateLimitError",
    "ValidationError",
    "APIError",
]
