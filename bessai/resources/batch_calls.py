"""Batch call resource — campaign management for outbound calling."""
from typing import List, Optional

from bessai._client import SyncHTTPClient, AsyncHTTPClient
from bessai.types.batch_call import (
    BatchCallResponse,
    BatchCallStatusResponse,
    BatchCallItemResponse,
    BatchCallCreateParams,
)

_BASE = "/v1/batch-calls"


class BatchCallResource:
    """Synchronous batch call resource.

    Usage::

        batch = client.batch_call.create(
            agent_id="ag_abc123",
            from_number="+905551234567",
            name="March Outreach",
            contacts=[{"phone_number": "+12125551001"}],
            max_concurrent_calls=10,
        )
        client.batch_call.start(batch.batch_call_id)
        status = client.batch_call.retrieve(batch.batch_call_id)
        items = client.batch_call.list_items(batch.batch_call_id)
    """

    def __init__(self, client: SyncHTTPClient):
        self._client = client

    # ------------------------------------------------------------------
    # Campaign CRUD
    # ------------------------------------------------------------------

    def create(self, **kwargs) -> BatchCallStatusResponse:
        """Create a batch call campaign.

        Args:
            agent_id: Agent to make the calls.
            from_number: Caller ID phone number (must be registered).
            contacts: List of ``BatchCallContact`` dicts with ``phone_number``
                and optional ``dynamic_variables``.
            name: Optional campaign name.
            max_concurrent_calls: Max simultaneous calls (1-100, default 5).
            retry_attempts: Retries per failed contact (0-5, default 1).
        """
        body = BatchCallCreateParams(**kwargs).to_api_params()
        data = self._client.post(_BASE, json=body)
        return BatchCallStatusResponse(**data)

    def retrieve(self, batch_call_id: str) -> BatchCallStatusResponse:
        """Get real-time batch call status with detailed counts."""
        data = self._client.get(f"{_BASE}/{batch_call_id}")
        return BatchCallStatusResponse(**data)

    def list(
        self,
        skip: int = 0,
        limit: int = 20,
        status: Optional[str] = None,
    ) -> List[BatchCallResponse]:
        """List batch call campaigns.

        Args:
            skip: Number of records to skip.
            limit: Maximum records to return (1-100).
            status: Filter by status (pending, queued, running, paused, completed, cancelled).
        """
        params: dict = {"skip": skip, "limit": limit}
        if status is not None:
            params["status"] = status
        data = self._client.get(_BASE, params=params)
        items = data if isinstance(data, list) else data.get("items", [])
        return [BatchCallResponse(**b) for b in items]

    def list_active(self) -> List[BatchCallStatusResponse]:
        """List only active (non-terminal) batch calls with real-time counts."""
        data = self._client.get(f"{_BASE}/active")
        items = data if isinstance(data, list) else data.get("items", [])
        return [BatchCallStatusResponse(**b) for b in items]

    def list_items(
        self,
        batch_call_id: str,
        status: Optional[str] = None,
        limit: int = 100,
    ) -> List[BatchCallItemResponse]:
        """Get individual contact results for a batch call.

        Args:
            batch_call_id: Batch call campaign ID.
            status: Filter items by status.
            limit: Maximum items to return (1-1000).
        """
        params: dict = {"limit": limit}
        if status is not None:
            params["status"] = status
        data = self._client.get(f"{_BASE}/{batch_call_id}/items", params=params)
        items = data if isinstance(data, list) else data.get("items", [])
        return [BatchCallItemResponse(**i) for i in items]

    def delete(self, batch_call_id: str) -> None:
        """Delete a batch call campaign (only if not running)."""
        self._client.delete(f"{_BASE}/{batch_call_id}")

    # ------------------------------------------------------------------
    # Lifecycle controls
    # ------------------------------------------------------------------

    def start(self, batch_call_id: str) -> BatchCallStatusResponse:
        """Start or resume a batch call campaign (queues for worker pickup)."""
        data = self._client.post(f"{_BASE}/{batch_call_id}/start")
        return BatchCallStatusResponse(**data)

    def pause(self, batch_call_id: str) -> BatchCallStatusResponse:
        """Pause a running batch. Active calls complete; no new calls initiated."""
        data = self._client.post(f"{_BASE}/{batch_call_id}/pause")
        return BatchCallStatusResponse(**data)

    def resume(self, batch_call_id: str) -> BatchCallStatusResponse:
        """Resume a paused batch call campaign."""
        data = self._client.post(f"{_BASE}/{batch_call_id}/resume")
        return BatchCallStatusResponse(**data)

    def cancel(self, batch_call_id: str) -> BatchCallStatusResponse:
        """Cancel a batch call. Pending items are marked as cancelled."""
        data = self._client.post(f"{_BASE}/{batch_call_id}/cancel")
        return BatchCallStatusResponse(**data)

    # Backward-compatible aliases
    def get(self, batch_call_id: str) -> BatchCallStatusResponse:
        """Alias for :meth:`retrieve`."""
        return self.retrieve(batch_call_id)

    def get_status(self, batch_call_id: str) -> BatchCallStatusResponse:
        """Alias for :meth:`retrieve`."""
        return self.retrieve(batch_call_id)

    def get_items(
        self, batch_call_id: str, status: Optional[str] = None, limit: int = 100
    ) -> List[BatchCallItemResponse]:
        """Alias for :meth:`list_items`."""
        return self.list_items(batch_call_id, status=status, limit=limit)


class AsyncBatchCallResource:
    """Asynchronous batch call resource (mirrors :class:`BatchCallResource`)."""

    def __init__(self, client: AsyncHTTPClient):
        self._client = client

    # ------------------------------------------------------------------
    # Campaign CRUD
    # ------------------------------------------------------------------

    async def create(self, **kwargs) -> BatchCallStatusResponse:
        body = BatchCallCreateParams(**kwargs).to_api_params()
        data = await self._client.post(_BASE, json=body)
        return BatchCallStatusResponse(**data)

    async def retrieve(self, batch_call_id: str) -> BatchCallStatusResponse:
        data = await self._client.get(f"{_BASE}/{batch_call_id}")
        return BatchCallStatusResponse(**data)

    async def list(
        self,
        skip: int = 0,
        limit: int = 20,
        status: Optional[str] = None,
    ) -> List[BatchCallResponse]:
        params: dict = {"skip": skip, "limit": limit}
        if status is not None:
            params["status"] = status
        data = await self._client.get(_BASE, params=params)
        items = data if isinstance(data, list) else data.get("items", [])
        return [BatchCallResponse(**b) for b in items]

    async def list_active(self) -> List[BatchCallStatusResponse]:
        data = await self._client.get(f"{_BASE}/active")
        items = data if isinstance(data, list) else data.get("items", [])
        return [BatchCallStatusResponse(**b) for b in items]

    async def list_items(
        self,
        batch_call_id: str,
        status: Optional[str] = None,
        limit: int = 100,
    ) -> List[BatchCallItemResponse]:
        params: dict = {"limit": limit}
        if status is not None:
            params["status"] = status
        data = await self._client.get(f"{_BASE}/{batch_call_id}/items", params=params)
        items = data if isinstance(data, list) else data.get("items", [])
        return [BatchCallItemResponse(**i) for i in items]

    async def delete(self, batch_call_id: str) -> None:
        await self._client.delete(f"{_BASE}/{batch_call_id}")

    # ------------------------------------------------------------------
    # Lifecycle controls
    # ------------------------------------------------------------------

    async def start(self, batch_call_id: str) -> BatchCallStatusResponse:
        data = await self._client.post(f"{_BASE}/{batch_call_id}/start")
        return BatchCallStatusResponse(**data)

    async def pause(self, batch_call_id: str) -> BatchCallStatusResponse:
        data = await self._client.post(f"{_BASE}/{batch_call_id}/pause")
        return BatchCallStatusResponse(**data)

    async def resume(self, batch_call_id: str) -> BatchCallStatusResponse:
        data = await self._client.post(f"{_BASE}/{batch_call_id}/resume")
        return BatchCallStatusResponse(**data)

    async def cancel(self, batch_call_id: str) -> BatchCallStatusResponse:
        data = await self._client.post(f"{_BASE}/{batch_call_id}/cancel")
        return BatchCallStatusResponse(**data)

    # Backward-compatible aliases
    async def get(self, batch_call_id: str) -> BatchCallStatusResponse:
        return await self.retrieve(batch_call_id)

    async def get_status(self, batch_call_id: str) -> BatchCallStatusResponse:
        return await self.retrieve(batch_call_id)

    async def get_items(
        self, batch_call_id: str, status: Optional[str] = None, limit: int = 100
    ) -> List[BatchCallItemResponse]:
        return await self.list_items(batch_call_id, status=status, limit=limit)


# Backward-compatible aliases
BatchCallsResource = BatchCallResource
AsyncBatchCallsResource = AsyncBatchCallResource
