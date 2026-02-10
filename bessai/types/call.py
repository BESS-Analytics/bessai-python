"""Call types for the BESS AI SDK."""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class Call(BaseModel):
    """Call record."""
    id: str
    call_type: Optional[str] = None
    status: Optional[str] = None
    agent_id: Optional[str] = None
    from_number: Optional[str] = None
    to_number: Optional[str] = None
    room_name: Optional[str] = None
    room_url: Optional[str] = None
    access_token: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    duration_seconds: Optional[int] = None
    transcript: Optional[Any] = None
    recording_url: Optional[str] = None
    call_summary: Optional[Dict[str, Any]] = None
    call_sentiment: Optional[Dict[str, Any]] = None
    call_cost: Optional[Dict[str, Any]] = None
    latency_metrics: Optional[Dict[str, Any]] = None
    processing_status: Optional[str] = None
    created_at: Optional[str] = None


class PhoneCallCreate(BaseModel):
    """Parameters for creating a phone call."""
    agent_id: str
    from_number: str
    to_number: str
    metadata: Optional[Dict[str, Any]] = None
    dynamic_variables: Optional[Dict[str, Any]] = None


class WebCallCreate(BaseModel):
    """Parameters for creating a web call."""
    agent_id: str
    metadata: Optional[Dict[str, Any]] = None
    dynamic_variables: Optional[Dict[str, Any]] = None


class CallListItem(BaseModel):
    """Call list item (lightweight)."""
    id: str
    call_type: Optional[str] = None
    status: Optional[str] = None
    agent_id: Optional[str] = None
    from_number: Optional[str] = None
    to_number: Optional[str] = None
    duration_seconds: Optional[int] = None
    processing_status: Optional[str] = None
    created_at: Optional[str] = None
