"""Billing resource — credits, usage tracking, and pricing.

Usage (sync)::

    balance  = client.billing.get_balance()
    ok       = client.billing.check_balance(required=5.0)
    txns     = client.billing.list_transactions(limit=20)
    usage    = client.billing.list_usage(event_type="voice_call")
    summary  = client.billing.get_usage_summary()
    daily    = client.billing.get_daily_usage(days=7)
    call_use = client.billing.get_call_usage("call_abc123")
    pricing  = client.billing.get_pricing()
    estimate = client.billing.estimate_pricing(llm_provider="openai", llm_model="gpt-4o")

Usage (async)::

    balance = await client.billing.get_balance()
"""
from typing import List, Optional, Union

from bessai._client import SyncHTTPClient, AsyncHTTPClient
from bessai.types.billing import (
    CreditBalanceResponse,
    BalanceCheckResponse,
    TransactionListResponse,
    CreditLedgerEntry,
    UsageListResponse,
    UsageEvent,
    UsageSummaryResponse,
    DailyUsageItem,
    CallUsageResponse,
    ServicePricingResponse,
    PricingEstimateParams,
    PricingEstimateResponse,
)


class BillingResource:
    """Sync billing resource — ``client.billing``."""

    def __init__(self, client: SyncHTTPClient):
        self._client = client

    # ------------------------------------------------------------------
    # Credit Balance
    # ------------------------------------------------------------------

    def get_balance(self) -> CreditBalanceResponse:
        """Get current credit balance for the organisation."""
        data = self._client.get("/v1/billing/balance")
        return CreditBalanceResponse(**data)

    def check_balance(self, required: float = 0.0) -> BalanceCheckResponse:
        """Check whether the balance is sufficient for an estimated cost.

        Args:
            required: The minimum balance required (USD).
        """
        params = {"required": required} if required else {}
        data = self._client.get("/v1/billing/balance/check", params=params)
        return BalanceCheckResponse(**data)

    # ------------------------------------------------------------------
    # Transactions (ledger)
    # ------------------------------------------------------------------

    def list_transactions(
        self,
        transaction_type: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> TransactionListResponse:
        """List credit-ledger transactions.

        Args:
            transaction_type: Filter by type (``credit_add``, ``usage_charge``,
                ``admin_adjustment``, ``refund``).
            limit: Page size (1–200, default 50).
            offset: Pagination offset.
        """
        params: dict = {"limit": limit, "offset": offset}
        if transaction_type is not None:
            params["type"] = transaction_type
        data = self._client.get("/v1/billing/transactions", params=params)
        return TransactionListResponse(**data)

    # ------------------------------------------------------------------
    # Usage
    # ------------------------------------------------------------------

    def list_usage(
        self,
        event_type: Optional[str] = None,
        reference_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> UsageListResponse:
        """List usage events with optional filters.

        Args:
            event_type: Filter by event type (``voice_call``, ``stt``,
                ``llm``, ``tts``, etc.).
            reference_id: Filter by reference ID (e.g. a call ID).
            start_date: ISO-format start date.
            end_date: ISO-format end date.
            limit: Page size (1–200, default 50).
            offset: Pagination offset.
        """
        params: dict = {"limit": limit, "offset": offset}
        for key, val in {
            "event_type": event_type,
            "reference_id": reference_id,
            "start_date": start_date,
            "end_date": end_date,
        }.items():
            if val is not None:
                params[key] = val
        data = self._client.get("/v1/billing/usage", params=params)
        return UsageListResponse(**data)

    def get_usage_summary(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> UsageSummaryResponse:
        """Get aggregated usage summary for a date range.

        Args:
            start_date: ISO-format start date.
            end_date: ISO-format end date.
        """
        params = {k: v for k, v in {
            "start_date": start_date, "end_date": end_date,
        }.items() if v is not None}
        data = self._client.get("/v1/billing/usage/summary", params=params)
        return UsageSummaryResponse(**data)

    def get_daily_usage(self, days: int = 30) -> List[DailyUsageItem]:
        """Get daily aggregated usage for charting.

        Args:
            days: Number of days to look back (1–365, default 30).
        """
        data = self._client.get("/v1/billing/usage/daily", params={"days": days})
        items = data if isinstance(data, list) else data.get("items", [])
        return [DailyUsageItem(**d) for d in items]

    def get_call_usage(self, call_id: str) -> CallUsageResponse:
        """Get all usage events for a specific call.

        Args:
            call_id: The call to look up.
        """
        data = self._client.get(f"/v1/billing/usage/call/{call_id}")
        return CallUsageResponse(**data)

    # ------------------------------------------------------------------
    # Pricing (public — no auth required)
    # ------------------------------------------------------------------

    def get_pricing(self) -> ServicePricingResponse:
        """Get all available service pricing."""
        data = self._client.get("/v1/billing/pricing")
        return ServicePricingResponse(**data)

    def estimate_pricing(
        self,
        agent_type: Optional[str] = None,
        stt_provider: Optional[str] = None,
        stt_model: Optional[str] = None,
        llm_provider: Optional[str] = None,
        llm_model: Optional[str] = None,
        voice_provider: Optional[str] = None,
        realtime_provider: Optional[str] = None,
        realtime_model: Optional[str] = None,
    ) -> PricingEstimateResponse:
        """Estimate per-minute pricing for an agent configuration.

        Pass provider/model combinations to see the estimated cost.
        """
        body = {k: v for k, v in {
            "agent_type": agent_type,
            "stt_provider": stt_provider,
            "stt_model": stt_model,
            "llm_provider": llm_provider,
            "llm_model": llm_model,
            "voice_provider": voice_provider,
            "realtime_provider": realtime_provider,
            "realtime_model": realtime_model,
        }.items() if v is not None}
        data = self._client.post("/v1/billing/pricing/estimate", json=body)
        return PricingEstimateResponse(**data)


class AsyncBillingResource:
    """Async billing resource — ``client.billing``."""

    def __init__(self, client: AsyncHTTPClient):
        self._client = client

    # ------------------------------------------------------------------
    # Credit Balance
    # ------------------------------------------------------------------

    async def get_balance(self) -> CreditBalanceResponse:
        """Get current credit balance for the organisation."""
        data = await self._client.get("/v1/billing/balance")
        return CreditBalanceResponse(**data)

    async def check_balance(self, required: float = 0.0) -> BalanceCheckResponse:
        """Check whether the balance is sufficient."""
        params = {"required": required} if required else {}
        data = await self._client.get("/v1/billing/balance/check", params=params)
        return BalanceCheckResponse(**data)

    # ------------------------------------------------------------------
    # Transactions
    # ------------------------------------------------------------------

    async def list_transactions(
        self,
        transaction_type: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> TransactionListResponse:
        """List credit-ledger transactions."""
        params: dict = {"limit": limit, "offset": offset}
        if transaction_type is not None:
            params["type"] = transaction_type
        data = await self._client.get("/v1/billing/transactions", params=params)
        return TransactionListResponse(**data)

    # ------------------------------------------------------------------
    # Usage
    # ------------------------------------------------------------------

    async def list_usage(
        self,
        event_type: Optional[str] = None,
        reference_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> UsageListResponse:
        """List usage events with optional filters."""
        params: dict = {"limit": limit, "offset": offset}
        for key, val in {
            "event_type": event_type,
            "reference_id": reference_id,
            "start_date": start_date,
            "end_date": end_date,
        }.items():
            if val is not None:
                params[key] = val
        data = await self._client.get("/v1/billing/usage", params=params)
        return UsageListResponse(**data)

    async def get_usage_summary(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> UsageSummaryResponse:
        """Get aggregated usage summary for a date range."""
        params = {k: v for k, v in {
            "start_date": start_date, "end_date": end_date,
        }.items() if v is not None}
        data = await self._client.get("/v1/billing/usage/summary", params=params)
        return UsageSummaryResponse(**data)

    async def get_daily_usage(self, days: int = 30) -> List[DailyUsageItem]:
        """Get daily aggregated usage for charting."""
        data = await self._client.get("/v1/billing/usage/daily", params={"days": days})
        items = data if isinstance(data, list) else data.get("items", [])
        return [DailyUsageItem(**d) for d in items]

    async def get_call_usage(self, call_id: str) -> CallUsageResponse:
        """Get all usage events for a specific call."""
        data = await self._client.get(f"/v1/billing/usage/call/{call_id}")
        return CallUsageResponse(**data)

    # ------------------------------------------------------------------
    # Pricing (public — no auth required)
    # ------------------------------------------------------------------

    async def get_pricing(self) -> ServicePricingResponse:
        """Get all available service pricing."""
        data = await self._client.get("/v1/billing/pricing")
        return ServicePricingResponse(**data)

    async def estimate_pricing(
        self,
        agent_type: Optional[str] = None,
        stt_provider: Optional[str] = None,
        stt_model: Optional[str] = None,
        llm_provider: Optional[str] = None,
        llm_model: Optional[str] = None,
        voice_provider: Optional[str] = None,
        realtime_provider: Optional[str] = None,
        realtime_model: Optional[str] = None,
    ) -> PricingEstimateResponse:
        """Estimate per-minute pricing for an agent configuration."""
        body = {k: v for k, v in {
            "agent_type": agent_type,
            "stt_provider": stt_provider,
            "stt_model": stt_model,
            "llm_provider": llm_provider,
            "llm_model": llm_model,
            "voice_provider": voice_provider,
            "realtime_provider": realtime_provider,
            "realtime_model": realtime_model,
        }.items() if v is not None}
        data = await self._client.post("/v1/billing/pricing/estimate", json=body)
        return PricingEstimateResponse(**data)
