"""Phone number types for the BESS AI SDK."""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class SIPConnection(BaseModel):
    """SIP connection for a phone number."""
    id: Optional[str] = None
    termination_uri: str
    username: Optional[str] = None
    password: Optional[str] = None
    nickname: Optional[str] = None
    connection_type: Optional[str] = "inbound"
    transport: Optional[str] = "TCP"
    sync_status: Optional[str] = None


class PhoneNumber(BaseModel):
    """Phone number entity."""
    id: str
    phone_number: str
    nickname: Optional[str] = None
    provider: Optional[str] = None
    inbound_agent_id: Optional[str] = None
    outbound_agent_id: Optional[str] = None
    status: Optional[str] = None
    sip_connections: Optional[List[SIPConnection]] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class PhoneNumberCreate(BaseModel):
    """Parameters for creating a phone number."""
    phone_number: str
    nickname: Optional[str] = None
    provider: Optional[str] = "custom"
    inbound_agent_id: Optional[str] = None
    outbound_agent_id: Optional[str] = None
    sip_connections: Optional[List[Dict[str, Any]]] = None


class PhoneNumberUpdate(BaseModel):
    """Parameters for updating a phone number."""
    nickname: Optional[str] = None
    inbound_agent_id: Optional[str] = None
    outbound_agent_id: Optional[str] = None
