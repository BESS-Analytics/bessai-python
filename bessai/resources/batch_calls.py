"""Batch calls resource — campaign management."""
from typing import Any, Dict, List, Optional

from bessai._client import SyncHTTPClient, AsyncHTTPClient
from bessai.types.batch_call import BatchCall, BatchCallCreate, BatchCallItem


class BatchCallsResource:
    """Sync batch calls resource."""

    def __init__(self, client: SyncHTTPClient):
        self._client = client

    def create(self, **kwargs) -> BatchCall:
        """Create a batch call campaign."""
        body = BatchCallCreate(**kwargs).model_dump(exclude_none=True)
        data = self._client.post("/v1/batch-calls", json=body)
        return BatchCall(**data)

    def list(self, skip: int = 0, limit: int = 20, status: Optional[str] = None) -> List[BatchCall]:
        """List batch call campaigns."""
        params = {"skip": skip, "limit": limit, "status": status}
        data = self._client.get("/v1/batch-calls", params=params)
        items = data if isinstance(data, list) else data.get("items", [])
        return [BatchCall(**b) for b in items]

    def get(self, batch_id: str) -> BatchCall:
        """Get batch call details."""
        data = self._client.get(f"/v1/batch-calls/{batch_id}")
        return BatchCall(**data)

    def get_status(self, batch_id: str) -> BatchCall:
        """Get batch call status."""
        data = self._client.get(f"/v1/batch-calls/{batch_id}/status")
        return BatchCall(**data)

    def get_items(self, batch_id: str, status: Optional[str] = None, limit: int = 100) -> List[BatchCallItem]:
        """Get items in a batch call."""
        params = {"status": status, "limit": limit}
        data = self._client.get(f"/v1/batch-calls/{batch_id}/items", params=params)
        items = data if isinstance(data, list) else data.get("items", [])
        return [BatchCallItem(**i) for i in items]

    def start(self, batch_id: str) -> BatchCall:
        """Start a batch call campaign."""
        data = self._client.post(f"/v1/batch-calls/{batch_id}/start")
        return BatchCall(**data)

    def pause(self, batch_id: str) -> BatchCall:
        """Pause a running batch call."""
        data = self._client.post(f"/v1/batch-calls/{batch_id}/pause")
        return BatchCall(**data)

    def resume(self, batch_id: str) -> BatchCall:
        """Resume a paused batch call."""
        data = self._client.post(f"/v1/batch-calls/{batch_id}/resume")
        return BatchCall(**data)

    def cancel(self, batch_id: str) -> BatchCall:
        """Cancel a batch call campaign."""
        data = self._client.post(f"/v1/batch-calls/{batch_id}/cancel")
        return BatchCall(**data)

    def delete(self, batch_id: str) -> None:
        """Delete a batch call campaign."""
        self._client.delete(f"/v1/batch-calls/{batch_id}")


class AsyncBatchCallsResource:
    """Async batch calls resource."""

    def __init__(self, client: AsyncHTTPClient):
        self._client = client

    async def create(self, **kwargs) -> BatchCall:
        body = BatchCallCreate(**kwargs).model_dump(exclude_none=True)
        data = await self._client.post("/v1/batch-calls", json=body)
        return BatchCall(**data)

    async def list(self, skip: int = 0, limit: int = 20, status: Optional[str] = None) -> List[BatchCall]:
        params = {"skip": skip, "limit": limit, "status": status}
        data = await self._client.get("/v1/batch-calls", params=params)
        items = data if isinstance(data, list) else data.get("items", [])
        return [BatchCall(**b) for b in items]

    async def get(self, batch_id: str) -> BatchCall:
        data = await self._client.get(f"/v1/batch-calls/{batch_id}")
        return BatchCall(**data)

    async def get_status(self, batch_id: str) -> BatchCall:
        data = await self._client.get(f"/v1/batch-calls/{batch_id}/status")
        return BatchCall(**data)

    async def get_items(self, batch_id: str, status: Optional[str] = None, limit: int = 100) -> List[BatchCallItem]:
        params = {"status": status, "limit": limit}
        data = await self._client.get(f"/v1/batch-calls/{batch_id}/items", params=params)
        items = data if isinstance(data, list) else data.get("items", [])
        return [BatchCallItem(**i) for i in items]

    async def start(self, batch_id: str) -> BatchCall:
        data = await self._client.post(f"/v1/batch-calls/{batch_id}/start")
        return BatchCall(**data)

    async def pause(self, batch_id: str) -> BatchCall:
        data = await self._client.post(f"/v1/batch-calls/{batch_id}/pause")
        return BatchCall(**data)

    async def resume(self, batch_id: str) -> BatchCall:
        data = await self._client.post(f"/v1/batch-calls/{batch_id}/resume")
        return BatchCall(**data)

    async def cancel(self, batch_id: str) -> BatchCall:
        data = await self._client.post(f"/v1/batch-calls/{batch_id}/cancel")
        return BatchCall(**data)

    async def delete(self, batch_id: str) -> None:
        await self._client.delete(f"/v1/batch-calls/{batch_id}")
