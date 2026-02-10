"""Analytics resource — metrics and reporting."""
from typing import List, Optional

from bessai._client import SyncHTTPClient, AsyncHTTPClient
from bessai.types.analytics import AnalyticsSummary, LatencyMetrics, CallsByDay


class AnalyticsResource:
    """Sync analytics resource."""

    def __init__(self, client: SyncHTTPClient):
        self._client = client

    def get_summary(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        agent_id: Optional[str] = None,
    ) -> AnalyticsSummary:
        """Get analytics summary for a time period."""
        params = {"from_date": from_date, "to_date": to_date, "agent_id": agent_id}
        data = self._client.get("/v1/analytics/summary", params=params)
        return AnalyticsSummary(**data)

    def get_latency(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        agent_id: Optional[str] = None,
    ) -> LatencyMetrics:
        """Get latency percentile metrics."""
        params = {"from_date": from_date, "to_date": to_date, "agent_id": agent_id}
        data = self._client.get("/v1/analytics/latency", params=params)
        return LatencyMetrics(**data)

    def get_calls_by_day(
        self,
        days: int = 30,
        agent_id: Optional[str] = None,
    ) -> List[CallsByDay]:
        """Get call counts grouped by day."""
        params = {"days": days, "agent_id": agent_id}
        data = self._client.get("/v1/analytics/calls-by-day", params=params)
        items = data if isinstance(data, list) else data.get("items", [])
        return [CallsByDay(**d) for d in items]


class AsyncAnalyticsResource:
    """Async analytics resource."""

    def __init__(self, client: AsyncHTTPClient):
        self._client = client

    async def get_summary(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        agent_id: Optional[str] = None,
    ) -> AnalyticsSummary:
        params = {"from_date": from_date, "to_date": to_date, "agent_id": agent_id}
        data = await self._client.get("/v1/analytics/summary", params=params)
        return AnalyticsSummary(**data)

    async def get_latency(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        agent_id: Optional[str] = None,
    ) -> LatencyMetrics:
        params = {"from_date": from_date, "to_date": to_date, "agent_id": agent_id}
        data = await self._client.get("/v1/analytics/latency", params=params)
        return LatencyMetrics(**data)

    async def get_calls_by_day(
        self,
        days: int = 30,
        agent_id: Optional[str] = None,
    ) -> List[CallsByDay]:
        params = {"days": days, "agent_id": agent_id}
        data = await self._client.get("/v1/analytics/calls-by-day", params=params)
        items = data if isinstance(data, list) else data.get("items", [])
        return [CallsByDay(**d) for d in items]
