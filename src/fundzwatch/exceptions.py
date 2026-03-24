"""Custom exceptions for FundzWatch SDK."""

from typing import Optional


class FundzWatchError(Exception):
    """Base exception for all FundzWatch errors."""

    def __init__(self, message: str, status_code: Optional[int] = None, error_code: Optional[str] = None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(message)


class AuthenticationError(FundzWatchError):
    """Raised when API key is invalid or missing."""
    pass


class RateLimitError(FundzWatchError):
    """Raised when monthly API call limit is exceeded."""
    pass


class ValidationError(FundzWatchError):
    """Raised when request parameters are invalid."""
    pass


class APIError(FundzWatchError):
    """Raised for unexpected API errors."""
    pass
