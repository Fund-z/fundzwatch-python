"""Custom exceptions for FundzWatch SDK."""


class FundzWatchError(Exception):
    """Base exception for all FundzWatch errors."""

    def __init__(self, message: str, status_code: int = None, error_code: str = None):
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
