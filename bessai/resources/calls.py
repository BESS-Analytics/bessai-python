"""Calls resource — phone/web call lifecycle."""
from typing import Any, Dict, List, Optional

from bessai._client import SyncHTTPClient, AsyncHTTPClient
from bessai.types.call import Call, PhoneCallCreate, WebCallCreate, CallListItem


class CallsResource:
    """Sync calls resource."""

    def __init__(self, client: SyncHTTPClient):
        self._client = client

    def create_phone_call(self, **kwargs) -> Call:
        """Create an outbound phone call."""
        body = PhoneCallCreate(**kwargs).model_dump(exclude_none=True)
        data = self._client.post("/v1/calls/phone", json=body)
        return Call(**data)

    def create_web_call(self, **kwargs) -> Call:
        """Create a web-based call (returns access token for browser)."""
        body = WebCallCreate(**kwargs).model_dump(exclude_none=True)
        data = self._client.post("/v1/calls/web", json=body)
        return Call(**data)

    def list(
        self,
        skip: int = 0,
        limit: int = 20,
        agent_id: Optional[str] = None,
        status: Optional[str] = None,
        call_type: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> List[CallListItem]:
        """List calls with optional filters."""
        params = {
            "skip": skip, "limit": limit, "agent_id": agent_id,
            "status": status, "call_type": call_type,
            "from_date": from_date, "to_date": to_date,
        }
        data = self._client.get("/v1/calls", params=params)
        items = data if isinstance(data, list) else data.get("items", [])
        return [CallListItem(**c) for c in items]

    def get(self, call_id: str) -> Call:
        """Get call details."""
        data = self._client.get(f"/v1/calls/{call_id}")
        return Call(**data)

    def end(self, call_id: str) -> Dict[str, Any]:
        """End an active call."""
        return self._client.post(f"/v1/calls/{call_id}/end")

    def delete(self, call_id: str) -> None:
        """Delete a call record."""
        self._client.delete(f"/v1/calls/{call_id}")

    def get_recording(self, call_id: str) -> Dict[str, Any]:
        """Get recording URL for a call."""
        return self._client.get(f"/v1/calls/{call_id}/recording")


class AsyncCallsResource:
    """Async calls resource."""

    def __init__(self, client: AsyncHTTPClient):
        self._client = client

    async def create_phone_call(self, **kwargs) -> Call:
        body = PhoneCallCreate(**kwargs).model_dump(exclude_none=True)
        data = await self._client.post("/v1/calls/phone", json=body)
        return Call(**data)

    async def create_web_call(self, **kwargs) -> Call:
        body = WebCallCreate(**kwargs).model_dump(exclude_none=True)
        data = await self._client.post("/v1/calls/web", json=body)
        return Call(**data)

    async def list(
        self,
        skip: int = 0,
        limit: int = 20,
        agent_id: Optional[str] = None,
        status: Optional[str] = None,
        call_type: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> List[CallListItem]:
        params = {
            "skip": skip, "limit": limit, "agent_id": agent_id,
            "status": status, "call_type": call_type,
            "from_date": from_date, "to_date": to_date,
        }
        data = await self._client.get("/v1/calls", params=params)
        items = data if isinstance(data, list) else data.get("items", [])
        return [CallListItem(**c) for c in items]

    async def get(self, call_id: str) -> Call:
        data = await self._client.get(f"/v1/calls/{call_id}")
        return Call(**data)

    async def end(self, call_id: str) -> Dict[str, Any]:
        return await self._client.post(f"/v1/calls/{call_id}/end")

    async def delete(self, call_id: str) -> None:
        await self._client.delete(f"/v1/calls/{call_id}")

    async def get_recording(self, call_id: str) -> Dict[str, Any]:
        return await self._client.get(f"/v1/calls/{call_id}/recording")
