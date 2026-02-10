"""API keys resource — key management."""
from typing import Any, Dict, List, Optional

from bessai._client import SyncHTTPClient, AsyncHTTPClient
from bessai.types.api_key import APIKey, APIKeyCreate, APIKeyCreated, APIKeyUpdate, APIKeyUsage


class APIKeysResource:
    """Sync API keys resource."""

    def __init__(self, client: SyncHTTPClient):
        self._client = client

    def create(self, **kwargs) -> APIKeyCreated:
        """Create a new API key. The full key is only returned once."""
        body = APIKeyCreate(**kwargs).model_dump(exclude_none=True)
        data = self._client.post("/v1/api-keys", json=body)
        return APIKeyCreated(**data)

    def list(
        self,
        skip: int = 0,
        limit: int = 20,
        include_inactive: bool = False,
    ) -> List[APIKey]:
        """List API keys (masked)."""
        params = {"skip": skip, "limit": limit, "include_inactive": include_inactive}
        data = self._client.get("/v1/api-keys", params=params)
        items = data.get("items", []) if isinstance(data, dict) else data
        return [APIKey(**k) for k in items]

    def get(self, key_id: str) -> APIKey:
        """Get API key details."""
        data = self._client.get(f"/v1/api-keys/{key_id}")
        return APIKey(**data)

    def update(self, key_id: str, **kwargs) -> APIKey:
        """Update API key name, scopes, or settings."""
        body = APIKeyUpdate(**kwargs).model_dump(exclude_none=True)
        data = self._client.patch(f"/v1/api-keys/{key_id}", json=body)
        return APIKey(**data)

    def delete(self, key_id: str) -> None:
        """Revoke an API key immediately."""
        self._client.delete(f"/v1/api-keys/{key_id}")

    def rotate(self, key_id: str, grace_period_hours: int = 24) -> APIKeyCreated:
        """Rotate an API key with a grace period for the old key."""
        body = {"grace_period_hours": grace_period_hours}
        data = self._client.post(f"/v1/api-keys/{key_id}/rotate", json=body)
        return APIKeyCreated(**data)

    def get_usage(self, key_id: str) -> APIKeyUsage:
        """Get usage statistics for an API key."""
        data = self._client.get(f"/v1/api-keys/{key_id}/usage")
        return APIKeyUsage(**data)


class AsyncAPIKeysResource:
    """Async API keys resource."""

    def __init__(self, client: AsyncHTTPClient):
        self._client = client

    async def create(self, **kwargs) -> APIKeyCreated:
        body = APIKeyCreate(**kwargs).model_dump(exclude_none=True)
        data = await self._client.post("/v1/api-keys", json=body)
        return APIKeyCreated(**data)

    async def list(
        self,
        skip: int = 0,
        limit: int = 20,
        include_inactive: bool = False,
    ) -> List[APIKey]:
        params = {"skip": skip, "limit": limit, "include_inactive": include_inactive}
        data = await self._client.get("/v1/api-keys", params=params)
        items = data.get("items", []) if isinstance(data, dict) else data
        return [APIKey(**k) for k in items]

    async def get(self, key_id: str) -> APIKey:
        data = await self._client.get(f"/v1/api-keys/{key_id}")
        return APIKey(**data)

    async def update(self, key_id: str, **kwargs) -> APIKey:
        body = APIKeyUpdate(**kwargs).model_dump(exclude_none=True)
        data = await self._client.patch(f"/v1/api-keys/{key_id}", json=body)
        return APIKey(**data)

    async def delete(self, key_id: str) -> None:
        await self._client.delete(f"/v1/api-keys/{key_id}")

    async def rotate(self, key_id: str, grace_period_hours: int = 24) -> APIKeyCreated:
        body = {"grace_period_hours": grace_period_hours}
        data = await self._client.post(f"/v1/api-keys/{key_id}/rotate", json=body)
        return APIKeyCreated(**data)

    async def get_usage(self, key_id: str) -> APIKeyUsage:
        data = await self._client.get(f"/v1/api-keys/{key_id}/usage")
        return APIKeyUsage(**data)
