"""Analytics resource — metrics and reporting.

Usage (sync)::

    summary = client.analytic.get_summary(from_date="2024-01-01")
    latency = client.analytic.get_latency(agent_id="ag_123")
    daily   = client.analytic.get_calls_by_day(days=7)

Usage (async)::

    summary = await client.analytic.get_summary()
"""
from typing import List, Optional

from bessai._client import SyncHTTPClient, AsyncHTTPClient
from bessai.types.analytics import AnalyticsSummary, LatencyMetrics, CallsByDay


class AnalyticResource:
    """Sync analytics resource — ``client.analytic``."""

    def __init__(self, client: SyncHTTPClient):
        self._client = client

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def get_summary(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        agent_id: Optional[str] = None,
    ) -> AnalyticsSummary:
        """Get analytics summary for a time period.

        Args:
            from_date: ISO-format start date (e.g. ``"2024-01-01"``).
            to_date: ISO-format end date.
            agent_id: Filter to a specific agent.
        """
        params = {k: v for k, v in {
            "from_date": from_date, "to_date": to_date, "agent_id": agent_id,
        }.items() if v is not None}
        data = self._client.get("/v1/analytics/summary", params=params)
        return AnalyticsSummary(**data)

    # ------------------------------------------------------------------
    # Latency
    # ------------------------------------------------------------------

    def get_latency(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        agent_id: Optional[str] = None,
    ) -> LatencyMetrics:
        """Get latency percentile metrics across pipeline stages.

        Args:
            from_date: ISO-format start date.
            to_date: ISO-format end date.
            agent_id: Filter to a specific agent.
        """
        params = {k: v for k, v in {
            "from_date": from_date, "to_date": to_date, "agent_id": agent_id,
        }.items() if v is not None}
        data = self._client.get("/v1/analytics/latency", params=params)
        return LatencyMetrics(**data)

    # ------------------------------------------------------------------
    # Calls by day
    # ------------------------------------------------------------------

    def get_calls_by_day(
        self,
        days: int = 30,
        agent_id: Optional[str] = None,
    ) -> List[CallsByDay]:
        """Get call counts grouped by day.

        Args:
            days: Number of days to look back (default 30).
            agent_id: Filter to a specific agent.
        """
        params: dict = {"days": days}
        if agent_id is not None:
            params["agent_id"] = agent_id
        data = self._client.get("/v1/analytics/calls-by-day", params=params)
        items = data if isinstance(data, list) else data.get("items", [])
        return [CallsByDay(**d) for d in items]


# Backward-compatible alias
AnalyticsResource = AnalyticResource


class AsyncAnalyticResource:
    """Async analytics resource — ``client.analytic``."""

    def __init__(self, client: AsyncHTTPClient):
        self._client = client

    async def get_summary(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        agent_id: Optional[str] = None,
    ) -> AnalyticsSummary:
        """Get analytics summary for a time period."""
        params = {k: v for k, v in {
            "from_date": from_date, "to_date": to_date, "agent_id": agent_id,
        }.items() if v is not None}
        data = await self._client.get("/v1/analytics/summary", params=params)
        return AnalyticsSummary(**data)

    async def get_latency(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        agent_id: Optional[str] = None,
    ) -> LatencyMetrics:
        """Get latency percentile metrics across pipeline stages."""
        params = {k: v for k, v in {
            "from_date": from_date, "to_date": to_date, "agent_id": agent_id,
        }.items() if v is not None}
        data = await self._client.get("/v1/analytics/latency", params=params)
        return LatencyMetrics(**data)

    async def get_calls_by_day(
        self,
        days: int = 30,
        agent_id: Optional[str] = None,
    ) -> List[CallsByDay]:
        """Get call counts grouped by day."""
        params: dict = {"days": days}
        if agent_id is not None:
            params["agent_id"] = agent_id
        data = await self._client.get("/v1/analytics/calls-by-day", params=params)
        items = data if isinstance(data, list) else data.get("items", [])
        return [CallsByDay(**d) for d in items]


# Backward-compatible alias
AsyncAnalyticsResource = AsyncAnalyticResource
