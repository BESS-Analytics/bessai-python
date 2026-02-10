"""API key types for the BESS AI SDK."""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class APIKey(BaseModel):
    """API key details (value is never shown after creation)."""
    id: str
    name: str
    key_prefix: str
    scopes: List[str] = ["*"]
    rate_limit_tier: str = "starter"
    ip_allowlist: List[str] = []
    is_active: bool = True
    usage_count: int = 0
    last_used_at: Optional[str] = None
    last_used_ip: Optional[str] = None
    expires_at: Optional[str] = None
    grace_period_ends_at: Optional[str] = None
    created_by: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class APIKeyCreated(BaseModel):
    """API key creation response — includes the full plaintext key."""
    id: str
    name: str
    key: str  # Full plaintext key — shown only once
    key_prefix: str
    scopes: List[str] = ["*"]
    rate_limit_tier: str = "starter"
    ip_allowlist: List[str] = []
    is_active: bool = True
    expires_at: Optional[str] = None
    created_at: Optional[str] = None
    message: str = ""


class APIKeyCreate(BaseModel):
    """Parameters for creating an API key."""
    name: str
    scopes: List[str] = ["*"]
    expires_in_days: Optional[int] = 365
    rate_limit_tier: str = "starter"
    ip_allowlist: List[str] = []


class APIKeyUpdate(BaseModel):
    """Parameters for updating an API key."""
    name: Optional[str] = None
    scopes: Optional[List[str]] = None
    rate_limit_tier: Optional[str] = None
    ip_allowlist: Optional[List[str]] = None
    is_active: Optional[bool] = None


class APIKeyUsage(BaseModel):
    """Usage statistics for an API key."""
    key_id: str
    key_name: str
    key_prefix: str
    total_requests: int = 0
    last_used_at: Optional[str] = None
    last_used_ip: Optional[str] = None
    rate_limit_tier: str = "starter"
    rate_limits: Dict[str, Any] = {}
    is_active: bool = True
    expires_at: Optional[str] = None
