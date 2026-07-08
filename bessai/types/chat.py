"""Chat types for the BESS AI SDK — text chat sessions over the voice agents' brain.

See ``docs/CHAT_AGENTS_SPEC.md`` and ``docs/API/REST_API_REFERENCE.md#chat-sessions``.
"""
from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field


# =============================================================================
# Response Models
# =============================================================================


class ChatMessage(BaseModel):
    """A single chat message row (user / assistant / tool / system)."""
    message_id: str = Field(alias="id")
    session_id: Optional[str] = None
    role: str = Field(description="user, assistant, tool, or system")
    content: Optional[str] = None
    tool_calls: Optional[List[Dict[str, Any]]] = None
    tokens_in: Optional[int] = None
    tokens_out: Optional[int] = None
    created_at: Optional[str] = None

    class Config:
        populate_by_name = True


class ChatSession(BaseModel):
    """Chat session record returned by ``create()``, ``list()``, and ``retrieve()``.

    ``transport="rest"`` sessions carry the agent's opening line in ``greeting``
    (``None`` if the agent has no greeting configured) — reply via ``send_message()``.
    ``transport="livekit"`` sessions carry ``access_token``/``room_url``/``room_name``
    for the client to join a text-only LiveKit room instead; ``greeting`` is ``None``
    there — the chat worker sends it over the room.
    """
    session_id: str = Field(alias="id")
    organization_id: str
    agent_id: str
    agent_version: Optional[int] = None
    channel_type: str = Field(description="api, web_widget, or dashboard_test")
    widget_id: Optional[str] = None
    external_user_key: Optional[str] = None
    status: str = Field(description="active, idle, or closed")
    livekit_room_name: Optional[str] = None
    message_count: int = 0
    agent_reply_count: int = 0
    total_tokens_in: int = 0
    total_tokens_out: int = 0
    summary: Optional[str] = None
    sentiment: Optional[str] = None
    session_cost: Optional[float] = None
    processing_status: Optional[str] = Field(
        None, description="queued, processing, done, or failed (post-chat pipeline).")
    started_at: Optional[str] = None
    last_message_at: Optional[str] = None
    closed_at: Optional[str] = None
    created_at: Optional[str] = None

    # create()/create_test_session() response only
    greeting: Optional[ChatMessage] = Field(
        None, description="First assistant message (transport='rest' only).")
    access_token: Optional[str] = Field(
        None, description="LiveKit JWT for the client to join the room (transport='livekit' only).")
    room_url: Optional[str] = Field(
        None, description="LiveKit WSS endpoint (transport='livekit' only).")
    room_name: Optional[str] = None

    class Config:
        populate_by_name = True


class ChatSessionDetail(ChatSession):
    """Session detail: summary fields + context + the paginated message thread."""
    dynamic_variables: Optional[Dict[str, Any]] = None
    session_metadata: Optional[Dict[str, Any]] = None
    messages: List[ChatMessage] = Field(default_factory=list)


class ChatTurnResult(BaseModel):
    """Response of ``send_message()`` — one user → assistant turn (REST transport)."""
    session_id: str
    assistant_content: str
    tool_calls: List[Dict[str, Any]] = Field(default_factory=list)
    tokens_in: int = 0
    tokens_out: int = 0
    session_closed: bool = Field(
        False, description="True if this turn closed the session (end_chat, message cap, or "
                            "insufficient credits).")
    close_reason: Optional[str] = Field(
        None, description="agent_end_chat, message_cap, insufficient_credits, or explicit_close.")
    user_message_id: Optional[str] = None
    assistant_message_id: Optional[str] = None


class ChatSessionCloseResult(BaseModel):
    """Response of ``close()``."""
    session_id: str
    status: str = "closed"


# =============================================================================
# Request Models
# =============================================================================


class ChatSessionCreateParams(BaseModel):
    """Parameters for creating a chat session.

    ``agent_id`` must be a **published** agent. ``transport="rest"`` (default) replies
    via ``send_message()``; ``transport="livekit"`` returns a token for a text-only room.
    """
    agent_id: str = Field(..., description="UUID of the published agent to use.")
    transport: Literal["rest", "livekit"] = Field(
        "rest", description="'rest' = synchronous send_message(); 'livekit' = text-only room.")
    channel_type: Literal["api", "web_widget", "dashboard_test"] = "api"
    dynamic_variables: Optional[Dict[str, str]] = Field(
        None, description="Key-value pairs injected into the agent's system prompt.")
    external_user_key: Optional[str] = Field(
        None, description="Your end-user's stable id — threads their sessions together.")

    def to_api_params(self) -> dict:
        return self.model_dump(exclude_none=True)


class ChatMessageCreateParams(BaseModel):
    """Parameters for sending a chat message. 1-4,000 characters."""
    content: str = Field(..., min_length=1, max_length=4000)

    def to_api_params(self) -> dict:
        return self.model_dump(exclude_none=True)


class ChatTestSessionCreateParams(BaseModel):
    """Parameters for a dashboard-style test chat session (mirrors ``TestCallCreateParams``).

    Accepts **draft** agents and a ``temp_config`` dict that overrides the agent's saved
    configuration without persisting it. REST transport only.
    """
    agent_id: str = Field(..., description="UUID of the agent (published or draft).")
    temp_config: Optional[Dict[str, Any]] = Field(
        None, description="Temporary config overrides (system_prompt, etc.). Not saved to the database.")
    dynamic_variables: Optional[Dict[str, str]] = Field(
        None, description="Key-value pairs injected into the agent's system prompt.")

    def to_api_params(self) -> dict:
        return self.model_dump(exclude_none=True)


# Backward-compatible aliases
ChatSessionResponse = ChatSession
ChatMessageResponse = ChatMessage
