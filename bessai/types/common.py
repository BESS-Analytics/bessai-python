"""Common types shared across all resources."""
from typing import Any, Dict, Generic, List, Optional, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated list response wrapper."""
    items: List[T] = []
    total: int = 0
    skip: int = 0
    limit: int = 20


class ErrorResponse(BaseModel):
    """API error response."""
    detail: str = ""
    status_code: Optional[int] = None
