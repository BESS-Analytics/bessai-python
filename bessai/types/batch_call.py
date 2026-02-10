"""Batch call types for the BESS AI SDK."""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class BatchCallContact(BaseModel):
    """Contact entry for a batch call campaign."""
    phone_number: str
    dynamic_variables: Optional[Dict[str, Any]] = None


class BatchCallCreate(BaseModel):
    """Parameters for creating a batch call campaign."""
    agent_id: str
    from_number: str
    contacts: List[BatchCallContact]
    max_concurrent_calls: int = 5
    retry_attempts: int = 1
    name: Optional[str] = None


class BatchCallItem(BaseModel):
    """Individual item in a batch call campaign."""
    id: str
    phone_number: str
    status: Optional[str] = None
    attempt_count: Optional[int] = None
    call_id: Optional[str] = None
    error_message: Optional[str] = None
    dynamic_variables: Optional[Dict[str, Any]] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None


class BatchCall(BaseModel):
    """Batch calling campaign."""
    id: str
    name: Optional[str] = None
    agent_id: Optional[str] = None
    from_number: Optional[str] = None
    total_count: int = 0
    completed_count: int = 0
    failed_count: int = 0
    max_concurrent: int = 5
    retry_attempts: int = 1
    status: Optional[str] = None
    progress_percent: Optional[float] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    created_at: Optional[str] = None
