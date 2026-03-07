"""
Call resource — phone, web, and test call lifecycle.

Function names follow Retell AI SDK conventions:
  client.call.create_phone_call(agent_id, from_number, to_number)
  client.call.create_web_call(agent_id)
  client.call.create_test_call(agent_id, temp_config=...)
  client.call.retrieve(call_id)
  client.call.list(agent_id=..., status=...)
  client.call.end(call_id)
  client.call.delete(call_id)
"""
from typing import Any, Dict, List, Optional

from bessai._client import SyncHTTPClient, AsyncHTTPClient
from bessai.types.call import (
    CallResponse,
    CallListItem,
    PhoneCallCreateParams,
    WebCallCreateParams,
    TestCallCreateParams,
)


class CallResource:
    """Synchronous call operations."""

    def __init__(self, client: SyncHTTPClient):
        self._client = client

    def create_phone_call(self, **kwargs) -> CallResponse:
        """Create an outbound phone call via SIP trunk.

        The agent must be published and ``from_number`` must be a phone
        number you own.  The call is placed immediately — no access token
        is returned (the callee connects via PSTN).

        Args:
            agent_id: UUID of the published agent.
            from_number: Caller ID in E.164 format (e.g. ``+14155551234``).
            to_number: Destination in E.164 format.
            metadata: Arbitrary metadata dict.
            dynamic_variables: Key-value pairs injected into the system prompt.
            batch_call_id: Link to a batch campaign (optional).
        """
        params = PhoneCallCreateParams(**kwargs)
        data = self._client.post("/v1/calls/phone", json=params.to_api_params())
        return CallResponse(**data)

    def create_web_call(self, **kwargs) -> CallResponse:
        """Create a browser-to-agent call via WebRTC.

        Returns ``access_token``, ``room_name``, and ``room_url``.
        Your frontend connects using the LiveKit client SDK::

            room = new Room()
            await room.connect(call.room_url, call.access_token)
            await room.localParticipant.setMicrophoneEnabled(true)

        The voice agent joins the room automatically.

        Args:
            agent_id: UUID of the published agent.
            metadata: Arbitrary metadata dict.
            dynamic_variables: Key-value pairs injected into the system prompt.
        """
        params = WebCallCreateParams(**kwargs)
        data = self._client.post("/v1/calls/web", json=params.to_api_params())
        return CallResponse(**data)

    def create_test_call(self, **kwargs) -> CallResponse:
        """Create a test call for development and agent testing.

        Like ``create_web_call`` but:
        - Accepts **draft (unpublished)** agents.
        - Accepts ``temp_config`` to override saved agent config without
          persisting changes.

        Args:
            agent_id: UUID of the agent (published or draft).
            temp_config: Dict of config overrides (system_prompt, voice_id, etc.).
            dynamic_variables: Key-value pairs injected into the system prompt.
        """
        params = TestCallCreateParams(**kwargs)
        data = self._client.post("/v1/calls/test", json=params.to_api_params())
        return CallResponse(**data)

    def retrieve(self, call_id: str) -> CallResponse:
        """Get full call details including transcript, analytics, and recordings.

        Args:
            call_id: UUID of the call.
        """
        data = self._client.get(f"/v1/calls/{call_id}")
        return CallResponse(**data)

    def list(
        self,
        skip: int = 0,
        limit: int = 20,
        agent_id: Optional[str] = None,
        status: Optional[str] = None,
        call_type: Optional[str] = None,
        batch_call_id: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> List[CallListItem]:
        """List calls with optional filters.

        Args:
            skip: Pagination offset (default 0).
            limit: Page size, 1-200 (default 20).
            agent_id: Filter by agent UUID.
            status: Filter by status (ended, connected, failed, etc.).
            call_type: Filter by type (inbound, outbound, web).
            batch_call_id: Filter by batch campaign UUID, ``"none"`` for
                single calls only, or ``"any"`` for batch calls only.
            from_date: ISO 8601 start date filter.
            to_date: ISO 8601 end date filter.
        """
        params: Dict[str, Any] = {"skip": skip, "limit": limit}
        if agent_id is not None:
            params["agent_id"] = agent_id
        if status is not None:
            params["status"] = status
        if call_type is not None:
            params["call_type"] = call_type
        if batch_call_id is not None:
            params["batch_call_id"] = batch_call_id
        if from_date is not None:
            params["from_date"] = from_date
        if to_date is not None:
            params["to_date"] = to_date

        data = self._client.get("/v1/calls", params=params)
        items = data if isinstance(data, list) else data.get("items", [])
        return [CallListItem(**c) for c in items]

    def end(self, call_id: str) -> Dict[str, Any]:
        """End an active call.

        Terminates the LiveKit room and triggers post-call processing.

        Args:
            call_id: UUID of the active call.
        """
        return self._client.post(f"/v1/calls/{call_id}/end")

    def delete(self, call_id: str) -> None:
        """Delete a call record.

        Args:
            call_id: UUID of the call.
        """
        self._client.delete(f"/v1/calls/{call_id}")

    def get_recording(self, call_id: str) -> bytes:
        """Download the call recording audio file.

        Returns raw audio bytes (typically OGG format).
        Use ``retrieve()`` to check if a recording exists first
        (``recording_url`` field).

        Args:
            call_id: UUID of the call.
        """
        return self._client.get_bytes(f"/v1/calls/{call_id}/recording")


class AsyncCallResource:
    """Asynchronous call operations."""

    def __init__(self, client: AsyncHTTPClient):
        self._client = client

    async def create_phone_call(self, **kwargs) -> CallResponse:
        """Create an outbound phone call via SIP trunk."""
        params = PhoneCallCreateParams(**kwargs)
        data = await self._client.post("/v1/calls/phone", json=params.to_api_params())
        return CallResponse(**data)

    async def create_web_call(self, **kwargs) -> CallResponse:
        """Create a browser-to-agent call via WebRTC."""
        params = WebCallCreateParams(**kwargs)
        data = await self._client.post("/v1/calls/web", json=params.to_api_params())
        return CallResponse(**data)

    async def create_test_call(self, **kwargs) -> CallResponse:
        """Create a test call for development."""
        params = TestCallCreateParams(**kwargs)
        data = await self._client.post("/v1/calls/test", json=params.to_api_params())
        return CallResponse(**data)

    async def retrieve(self, call_id: str) -> CallResponse:
        """Get full call details."""
        data = await self._client.get(f"/v1/calls/{call_id}")
        return CallResponse(**data)

    async def list(
        self,
        skip: int = 0,
        limit: int = 20,
        agent_id: Optional[str] = None,
        status: Optional[str] = None,
        call_type: Optional[str] = None,
        batch_call_id: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> List[CallListItem]:
        """List calls with optional filters."""
        params: Dict[str, Any] = {"skip": skip, "limit": limit}
        if agent_id is not None:
            params["agent_id"] = agent_id
        if status is not None:
            params["status"] = status
        if call_type is not None:
            params["call_type"] = call_type
        if batch_call_id is not None:
            params["batch_call_id"] = batch_call_id
        if from_date is not None:
            params["from_date"] = from_date
        if to_date is not None:
            params["to_date"] = to_date

        data = await self._client.get("/v1/calls", params=params)
        items = data if isinstance(data, list) else data.get("items", [])
        return [CallListItem(**c) for c in items]

    async def end(self, call_id: str) -> Dict[str, Any]:
        """End an active call."""
        return await self._client.post(f"/v1/calls/{call_id}/end")

    async def delete(self, call_id: str) -> None:
        """Delete a call record."""
        await self._client.delete(f"/v1/calls/{call_id}")

    async def get_recording(self, call_id: str) -> bytes:
        """Download the call recording audio file."""
        return await self._client.get_bytes(f"/v1/calls/{call_id}/recording")


# Backward-compatible aliases
CallsResource = CallResource
AsyncCallsResource = AsyncCallResource
