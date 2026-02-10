"""
BESS AI SDK Exception Hierarchy.

All exceptions inherit from BessAIError for easy catch-all handling.
"""
from typing import Optional, Any, Dict


class BessAIError(Exception):
    """Base exception for all BESS AI SDK errors."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        body: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.body = body or {}
        super().__init__(self.message)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(status_code={self.status_code}, message={self.message!r})"


class AuthenticationError(BessAIError):
    """Raised when API key is invalid, expired, or missing (HTTP 401)."""

    def __init__(self, message: str = "Invalid or expired API key", **kwargs):
        super().__init__(message, status_code=401, **kwargs)


class PermissionDeniedError(BessAIError):
    """Raised when API key lacks required scope (HTTP 403)."""

    def __init__(self, message: str = "Permission denied", **kwargs):
        super().__init__(message, status_code=403, **kwargs)


class NotFoundError(BessAIError):
    """Raised when the requested resource does not exist (HTTP 404)."""

    def __init__(self, message: str = "Resource not found", **kwargs):
        super().__init__(message, status_code=404, **kwargs)


class ValidationError(BessAIError):
    """Raised when request validation fails (HTTP 422)."""

    def __init__(
        self,
        message: str = "Validation error",
        errors: Optional[list] = None,
        **kwargs,
    ):
        self.errors = errors or []
        super().__init__(message, status_code=422, **kwargs)


class RateLimitError(BessAIError):
    """Raised when rate limit is exceeded (HTTP 429)."""

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after: Optional[float] = None,
        **kwargs,
    ):
        self.retry_after = retry_after
        super().__init__(message, status_code=429, **kwargs)


class InternalServerError(BessAIError):
    """Raised when the BESS AI server returns 5xx (HTTP 500+)."""

    def __init__(self, message: str = "Internal server error", **kwargs):
        super().__init__(message, status_code=500, **kwargs)


class ConnectionError(BessAIError):
    """Raised when the SDK cannot reach the BESS AI server."""

    def __init__(self, message: str = "Could not connect to BESS AI", **kwargs):
        super().__init__(message, **kwargs)


class TimeoutError(BessAIError):
    """Raised when a request times out."""

    def __init__(self, message: str = "Request timed out", **kwargs):
        super().__init__(message, **kwargs)


# Map HTTP status codes to exception classes
STATUS_CODE_MAP = {
    401: AuthenticationError,
    403: PermissionDeniedError,
    404: NotFoundError,
    422: ValidationError,
    429: RateLimitError,
}


def raise_for_status(status_code: int, body: Optional[Dict[str, Any]] = None) -> None:
    """Raise the appropriate exception for an HTTP error status code."""
    if status_code < 400:
        return

    body = body or {}
    detail = body.get("detail", "")
    if isinstance(detail, list):
        # FastAPI validation error format
        message = "; ".join(
            f"{e.get('loc', ['?'])[-1]}: {e.get('msg', '?')}" for e in detail
        )
        raise ValidationError(message=message, errors=detail, body=body)

    message = str(detail) if detail else f"HTTP {status_code}"

    exc_class = STATUS_CODE_MAP.get(status_code)
    if exc_class:
        if exc_class == RateLimitError:
            raise RateLimitError(message=message, body=body)
        raise exc_class(message=message, body=body)

    if status_code >= 500:
        raise InternalServerError(message=message, body=body)

    raise BessAIError(message=message, status_code=status_code, body=body)
