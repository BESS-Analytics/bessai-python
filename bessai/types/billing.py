"""Billing & credit types for the BESS AI SDK."""
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel


# =========================================================================
# Credit Balance
# =========================================================================

class CreditBalanceResponse(BaseModel):
    """Current credit balance for the organisation."""
    current_balance: float
    total_credits_added: float
    total_credits_used: float
    organization_id: str


class BalanceCheckResponse(BaseModel):
    """Result of a balance-sufficiency check."""
    sufficient: bool
    balance: float
    required: float
    min_balance: float
    shortfall: float


# =========================================================================
# Transaction Ledger
# =========================================================================

class CreditLedgerEntry(BaseModel):
    """A single credit-ledger entry."""
    id: UUID
    organization_id: UUID
    transaction_type: str
    amount_usd: float
    balance_before: float
    balance_after: float
    description: Optional[str] = None
    reference_id: Optional[str] = None
    reference_type: Optional[str] = None
    metadata: Dict[str, Any] = {}
    created_at: datetime


class TransactionListResponse(BaseModel):
    """Paginated list of credit-ledger entries."""
    entries: List[CreditLedgerEntry]
    total: int
    limit: int
    offset: int


# =========================================================================
# Usage
# =========================================================================

class UsageEvent(BaseModel):
    """A single usage event."""
    id: UUID
    organization_id: UUID
    event_type: str
    reference_id: str
    reference_type: str
    provider: Optional[str] = None
    model: Optional[str] = None
    usage_data: Dict[str, Any] = {}
    cost_usd: float
    price_usd: float
    pricing_data: Dict[str, Any] = {}
    created_at: datetime


class UsageListResponse(BaseModel):
    """Paginated list of usage events."""
    events: List[UsageEvent]
    total: int
    limit: int
    offset: int


class UsageSummaryResponse(BaseModel):
    """Aggregated usage summary for a period."""
    organization_id: str
    period: Dict[str, str]
    total_events: int
    total_cost_usd: float
    total_price_usd: float
    breakdown: Dict[str, Any]


class DailyUsageItem(BaseModel):
    """Daily aggregated usage."""
    date: str
    event_count: int
    total_cost_usd: float
    total_price_usd: float


class CallUsageResponse(BaseModel):
    """All usage events for a specific call."""
    call_id: str
    events: List[UsageEvent]
    total_cost_usd: float
    total_price_usd: float


# =========================================================================
# Pricing
# =========================================================================

class ServicePricingResponse(BaseModel):
    """All available service pricing."""
    voice_call_pricing: Dict[str, Any]
    service_pricing: Dict[str, Any]
    credit_config: Dict[str, Any]


class PricingEstimateParams(BaseModel):
    """Parameters for estimating per-minute voice call pricing."""
    agent_type: Optional[str] = "voice_agent"
    stt_provider: Optional[str] = "deepgram"
    stt_model: Optional[str] = None
    llm_provider: Optional[str] = "groq"
    llm_model: Optional[str] = None
    voice_provider: Optional[str] = "elevenlabs"
    realtime_provider: Optional[str] = None
    realtime_model: Optional[str] = None

    def to_api_params(self) -> dict:
        """Convert to API request body, omitting None values."""
        return {k: v for k, v in self.model_dump().items() if v is not None}


class PricingEstimateResponse(BaseModel):
    """Per-minute pricing estimate for an agent configuration."""
    total_per_minute: float
    pricing_type: str
    components: Dict[str, float]
    post_call_analytics_per_execution: Optional[float] = None
