"""Phone number types for the BESS AI SDK."""
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------------
# SIP Connection (child of PhoneNumber)
# ---------------------------------------------------------------------------

class SIPConnectionResponse(BaseModel):
    """SIP connection attached to a phone number."""

    model_config = ConfigDict(populate_by_name=True)

    sip_connection_id: str = Field(alias="id")
    phone_number_id: str
    termination_uri: str
    username: Optional[str] = None
    nickname: Optional[str] = None
    connection_type: str  # inbound | outbound | both
    transport: str  # TCP | UDP | TLS

    # LiveKit sync
    livekit_trunk_id: Optional[str] = None
    sync_status: str = "pending"  # pending | synced | failed
    sync_error: Optional[str] = None

    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class SIPConnectionCreateParams(BaseModel):
    """Parameters for creating a SIP connection."""

    termination_uri: str
    username: Optional[str] = None
    password: Optional[str] = None
    nickname: Optional[str] = None
    connection_type: str = "inbound"  # inbound | outbound | both
    transport: str = "TCP"  # TCP | UDP | TLS

    def to_api_params(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)


class SIPConnectionUpdateParams(BaseModel):
    """Parameters for updating a SIP connection."""

    termination_uri: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    nickname: Optional[str] = None
    connection_type: Optional[str] = None
    transport: Optional[str] = None

    def to_api_params(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)


# ---------------------------------------------------------------------------
# SIP Dispatch Rule (read-only, returned in detail view)
# ---------------------------------------------------------------------------

class SIPDispatchRuleResponse(BaseModel):
    """SIP dispatch rule for inbound call routing."""

    model_config = ConfigDict(populate_by_name=True)

    dispatch_rule_id: str = Field(alias="id")
    name: str
    description: Optional[str] = None
    rule_type: str  # direct | individual
    room_name: Optional[str] = None
    room_prefix: Optional[str] = None
    agent_id: Optional[str] = None
    hide_phone_number: bool = False
    auto_answer: bool = True
    ring_timeout_seconds: int = 30
    priority: int = 0

    # LiveKit sync
    livekit_rule_id: Optional[str] = None
    livekit_sync_status: str = "pending"
    livekit_sync_error: Optional[str] = None

    status: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


# ---------------------------------------------------------------------------
# Phone Number — Response (list view)
# ---------------------------------------------------------------------------

class PhoneNumberResponse(BaseModel):
    """Phone number returned by list endpoint."""

    model_config = ConfigDict(populate_by_name=True)

    phone_number_id: str = Field(alias="id")
    phone_number: str
    nickname: Optional[str] = None
    provider: str = "custom"

    # Agent assignments
    inbound_agent_id: Optional[str] = None
    outbound_agent_id: Optional[str] = None

    status: str = "active"
    created_at: Optional[str] = None


# ---------------------------------------------------------------------------
# Phone Number — Detail Response (single-item view)
# ---------------------------------------------------------------------------

class PhoneNumberDetailResponse(BaseModel):
    """Phone number returned by retrieve endpoint (includes nested resources)."""

    model_config = ConfigDict(populate_by_name=True)

    phone_number_id: str = Field(alias="id")
    phone_number: str
    nickname: Optional[str] = None
    provider: str = "custom"

    # Agent assignments with resolved names
    inbound_agent_id: Optional[str] = None
    inbound_agent_name: Optional[str] = None
    outbound_agent_id: Optional[str] = None
    outbound_agent_name: Optional[str] = None

    # Country restrictions
    allowed_inbound_countries: List[str] = Field(default_factory=lambda: ["*"])
    allowed_outbound_countries: List[str] = Field(default_factory=lambda: ["*"])

    # Webhooks
    inbound_webhook_url: Optional[str] = None

    # Nested resources
    sip_connections: List[SIPConnectionResponse] = Field(default_factory=list)
    dispatch_rules: List[SIPDispatchRuleResponse] = Field(default_factory=list)

    status: str = "active"
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


# ---------------------------------------------------------------------------
# Phone Number — Create / Update params
# ---------------------------------------------------------------------------

class PhoneNumberCreateParams(BaseModel):
    """Parameters for creating a phone number."""

    phone_number: str
    nickname: Optional[str] = None
    provider: str = "custom"  # custom | netgsm | twilio | telnyx

    # Agent assignments
    inbound_agent_id: Optional[str] = None
    outbound_agent_id: Optional[str] = None

    # Country restrictions
    allowed_inbound_countries: Optional[List[str]] = None
    allowed_outbound_countries: Optional[List[str]] = None

    # Webhooks
    inbound_webhook_url: Optional[str] = None

    def to_api_params(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)


class PhoneNumberUpdateParams(BaseModel):
    """Parameters for updating a phone number."""

    nickname: Optional[str] = None
    provider: Optional[str] = None

    # Agent assignments
    inbound_agent_id: Optional[str] = None
    outbound_agent_id: Optional[str] = None

    # Country restrictions
    allowed_inbound_countries: Optional[List[str]] = None
    allowed_outbound_countries: Optional[List[str]] = None

    # Webhooks
    inbound_webhook_url: Optional[str] = None

    def to_api_params(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)


class PhoneNumberAgentUpdateParams(BaseModel):
    """Parameters for quick agent assignment update."""

    inbound_agent_id: Optional[str] = None
    outbound_agent_id: Optional[str] = None

    def to_api_params(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)


# ---------------------------------------------------------------------------
# Backward-compatibility aliases
# ---------------------------------------------------------------------------
PhoneNumber = PhoneNumberResponse
SIPConnection = SIPConnectionResponse
PhoneNumberCreate = PhoneNumberCreateParams
PhoneNumberUpdate = PhoneNumberUpdateParams
