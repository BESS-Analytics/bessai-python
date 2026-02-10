"""
BESS AI SDK — WebSocket Streaming Helpers.

Provides managed WebSocket connections for real-time events
like batch call status updates.
"""
import json
import asyncio
from typing import Any, AsyncIterator, Callable, Dict, Optional

from bessai._config import ClientConfig


class BatchCallStream:
    """
    Async iterator for real-time batch call status updates via WebSocket.

    Usage:
        async for event in client.streaming.batch_call_status(campaign_id):
            print(event)
    """

    def __init__(self, config: ClientConfig, campaign_id: str):
        self._config = config
        self._campaign_id = campaign_id
        self._ws = None

    def _build_ws_url(self) -> str:
        """Convert HTTP base URL to WebSocket URL."""
        base = self._config.base_url
        if base.startswith("https://"):
            ws_base = "wss://" + base[8:]
        elif base.startswith("http://"):
            ws_base = "ws://" + base[7:]
        else:
            ws_base = base
        return f"{ws_base}/ws/batch-call/{self._campaign_id}?token={self._config.api_key}"

    async def connect(self) -> "BatchCallStream":
        """Open the WebSocket connection."""
        import websockets
        url = self._build_ws_url()
        self._ws = await websockets.connect(url)
        return self

    async def __aiter__(self) -> AsyncIterator[Dict[str, Any]]:
        """Iterate over incoming WebSocket messages."""
        if not self._ws:
            await self.connect()
        try:
            async for message in self._ws:
                try:
                    yield json.loads(message)
                except json.JSONDecodeError:
                    yield {"raw": message}
        except Exception:
            pass
        finally:
            await self.close()

    async def close(self) -> None:
        """Close the WebSocket connection."""
        if self._ws:
            await self._ws.close()
            self._ws = None

    async def __aenter__(self) -> "BatchCallStream":
        await self.connect()
        return self

    async def __aexit__(self, *args) -> None:
        await self.close()


class StreamingResource:
    """
    Streaming resource for real-time WebSocket connections.

    Usage (async only):
        async with client.streaming.batch_call_status("campaign-id") as stream:
            async for event in stream:
                print(event["status"])
    """

    def __init__(self, config: ClientConfig):
        self._config = config

    def batch_call_status(self, campaign_id: str) -> BatchCallStream:
        """
        Stream real-time status updates for a batch call campaign.

        Args:
            campaign_id: The batch call campaign ID.

        Returns:
            BatchCallStream: Async context manager / async iterator.
        """
        return BatchCallStream(self._config, campaign_id)
