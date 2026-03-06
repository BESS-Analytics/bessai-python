"""Call types for the BESS AI SDK."""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# =============================================================================
# Response Models
# =============================================================================


class WorkflowExecutionSummary(BaseModel):
    """Summary of a workflow that executed during a call."""
    id: str
    workflow_id: str
    workflow_name: Optional[str] = None
    status: str = Field(description="running, success, failed, timeout, skipped")
    trigger_type: str
    trigger_source: Optional[str] = None
    execution_time_ms: Optional[int] = None
    error_message: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None


class CallResponse(BaseModel):
    """Call record returned by the API.

    For web/test calls the response includes ``access_token``, ``room_name``
    and ``room_url`` which the client uses to connect via LiveKit WebRTC.
    For phone calls these fields are ``null``.
    """
    call_id: str = Field(alias="id")
    call_type: str = Field(description="inbound, outbound, or web")
    status: str = Field(description="waiting, queued, initiating, ringing, connected, ended, failed")
    agent_id: str

    # Phone numbers (phone calls only)
    from_number: Optional[str] = None
    to_number: Optional[str] = None

    # WebRTC connection (web/test calls only)
    access_token: Optional[str] = Field(None, description="LiveKit JWT for client to join the room.")
    room_name: Optional[str] = Field(None, description="LiveKit room identifier.")
    room_url: Optional[str] = Field(None, description="LiveKit WSS endpoint for WebRTC connection.")

    # Timing
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    duration_seconds: Optional[int] = None

    # Content (populated after call ends)
    transcript: Optional[List[Dict[str, Any]]] = None
    recording_url: Optional[str] = None

    # Post-call analytics
    call_analysis: Optional[Dict[str, Any]] = Field(None, description="Custom post-call extraction results.")
    call_summary: Optional[Dict[str, Any]] = None
    call_sentiment: Optional[Dict[str, Any]] = None
    call_cost: Optional[Dict[str, Any]] = None
    latency_metrics: Optional[Dict[str, Any]] = None
    processing_status: Optional[str] = Field(None, description="pending, processing, completed, failed")

    # Workflow executions
    workflow_executions: Optional[List[WorkflowExecutionSummary]] = None

    created_at: str

    class Config:
        populate_by_name = True


class CallListItem(BaseModel):
    """Lightweight call item returned by the list endpoint."""
    call_id: str = Field(alias="id")
    call_type: str
    status: str
    agent_id: Optional[str] = None
    agent_name: Optional[str] = None
    from_number: Optional[str] = None
    to_number: Optional[str] = None
    duration_seconds: Optional[int] = None
    start_time: Optional[str] = None
    created_at: str

    class Config:
        populate_by_name = True


# =============================================================================
# Request Models
# =============================================================================


class PhoneCallCreateParams(BaseModel):
    """Parameters for creating an outbound phone call.

    The agent must be published before it can receive calls.
    Phone numbers must be in E.164 format (e.g. ``+14155551234``).
    """
    agent_id: str = Field(..., description="UUID of the published agent to use.")
    from_number: str = Field(..., pattern=r"^\+?[1-9]\d{1,14}$",
                             description="Caller ID in E.164 format. Must be a number you own.")
    to_number: str = Field(..., pattern=r"^\+?[1-9]\d{1,14}$",
                           description="Destination phone number in E.164 format.")
    metadata: Optional[Dict[str, Any]] = Field(None,
                                               description="Arbitrary metadata attached to the call.")
    dynamic_variables: Optional[Dict[str, str]] = Field(None,
                                                        description="Key-value pairs injected into the agent's system prompt.")
    batch_call_id: Optional[str] = Field(None,
                                         description="Link this call to a batch campaign.")

    def to_api_params(self) -> dict:
        return self.model_dump(exclude_none=True)


class WebCallCreateParams(BaseModel):
    """Parameters for creating a web call (browser-to-agent via WebRTC).

    Returns ``access_token`` and ``room_url`` which your frontend uses
    to connect via the LiveKit client SDK.  The agent joins automatically.
    """
    agent_id: str = Field(..., description="UUID of the published agent to use.")
    metadata: Optional[Dict[str, Any]] = Field(None,
                                               description="Arbitrary metadata attached to the call.")
    dynamic_variables: Optional[Dict[str, str]] = Field(None,
                                                        description="Key-value pairs injected into the agent's system prompt.")

    def to_api_params(self) -> dict:
        return self.model_dump(exclude_none=True)


class TestCallCreateParams(BaseModel):
    """Parameters for creating a test call.

    Like a web call but accepts **draft (unpublished) agents** and an optional
    ``temp_config`` dict that overrides the agent's saved configuration.
    Used for testing agents during development.
    """
    agent_id: str = Field(..., description="UUID of the agent (published or draft).")
    temp_config: Optional[Dict[str, Any]] = Field(None,
                                                   description="Temporary config overrides (system_prompt, voice_id, etc.). "
                                                               "Not saved to the database.")
    dynamic_variables: Optional[Dict[str, str]] = Field(None,
                                                        description="Key-value pairs injected into the agent's system prompt.")

    def to_api_params(self) -> dict:
        return self.model_dump(exclude_none=True)


# Backward-compatible aliases
Call = CallResponse
PhoneCallCreate = PhoneCallCreateParams
WebCallCreate = WebCallCreateParams
