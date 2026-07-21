"""Widgets resource — the embeddable voice/chat widget.

Create a widget for a published agent and drop ``widget.embed_code`` (a
ready-to-paste ``<script>`` tag) into any website — no dashboard visit needed::

    widget = client.widget.create(agent_id=agent.agent_id, name="Site widget",
                                  mode="hybrid", locale="en")
    print(widget.embed_code)
    # <script src="https://api.bess-ai.com/embed.js" data-widget-id="bess_pk_live_..." async></script>

Widget creation is entitlement-gated (one-time unlock per mode): a 402 means
the feature isn't unlocked yet — check ``get_entitlement()`` and unlock from
the console.
"""
from typing import List, Optional

from bessai._client import SyncHTTPClient, AsyncHTTPClient
from bessai.types.widget import (
    Widget,
    WidgetCreateParams,
    WidgetEntitlement,
)

_BASE = "/v1/widgets"


class WidgetResource:
    """Sync widgets resource — ``client.widget``."""

    def __init__(self, client: SyncHTTPClient):
        self._client = client

    def create(self, **kwargs) -> Widget:
        """Create a widget for a PUBLISHED agent. Returns the widget incl.
        ``public_key`` and the ready-to-paste ``embed_code`` snippet."""
        body = WidgetCreateParams(**kwargs).model_dump(exclude_none=True)
        data = self._client.post(_BASE, json=body)
        return Widget(**data)

    def list(self, skip: int = 0, limit: int = 20, include_inactive: bool = True) -> List[Widget]:
        """List widgets."""
        data = self._client.get(
            _BASE, params={"skip": skip, "limit": limit, "include_inactive": include_inactive}
        )
        items = data if isinstance(data, list) else data.get("items", [])
        return [Widget(**w) for w in items]

    def retrieve(self, widget_id: str) -> Widget:
        """Get widget details (incl. ``embed_code``)."""
        data = self._client.get(f"{_BASE}/{widget_id}")
        return Widget(**data)

    # Alias, matching the other resources' convention
    get = retrieve

    def update(self, widget_id: str, **kwargs) -> Widget:
        """Update origins/branding/caps/mode/is_active. ``embed_code`` in the
        response reflects the new branding — re-paste it if it changed."""
        body = {k: v for k, v in kwargs.items() if v is not None}
        data = self._client.patch(f"{_BASE}/{widget_id}", json=body)
        return Widget(**data)

    def delete(self, widget_id: str) -> None:
        """Delete a widget. Its publishable key stops working immediately."""
        self._client.delete(f"{_BASE}/{widget_id}")

    def rotate(self, widget_id: str) -> Widget:
        """Rotate the publishable key. The old key stops working immediately —
        re-paste the returned ``embed_code``."""
        data = self._client.post(f"{_BASE}/{widget_id}/rotate")
        return Widget(**data)

    def get_entitlement(self) -> WidgetEntitlement:
        """Unlock state + price of the widget features ('widget', 'chat_widget')."""
        data = self._client.get(f"{_BASE}/entitlement")
        return WidgetEntitlement(**data)


class AsyncWidgetResource:
    """Async widgets resource — ``client.widget``."""

    def __init__(self, client: AsyncHTTPClient):
        self._client = client

    async def create(self, **kwargs) -> Widget:
        """Create a widget for a PUBLISHED agent."""
        body = WidgetCreateParams(**kwargs).model_dump(exclude_none=True)
        data = await self._client.post(_BASE, json=body)
        return Widget(**data)

    async def list(self, skip: int = 0, limit: int = 20, include_inactive: bool = True) -> List[Widget]:
        data = await self._client.get(
            _BASE, params={"skip": skip, "limit": limit, "include_inactive": include_inactive}
        )
        items = data if isinstance(data, list) else data.get("items", [])
        return [Widget(**w) for w in items]

    async def retrieve(self, widget_id: str) -> Widget:
        data = await self._client.get(f"{_BASE}/{widget_id}")
        return Widget(**data)

    get = retrieve

    async def update(self, widget_id: str, **kwargs) -> Widget:
        body = {k: v for k, v in kwargs.items() if v is not None}
        data = await self._client.patch(f"{_BASE}/{widget_id}", json=body)
        return Widget(**data)

    async def delete(self, widget_id: str) -> None:
        await self._client.delete(f"{_BASE}/{widget_id}")

    async def rotate(self, widget_id: str) -> Widget:
        data = await self._client.post(f"{_BASE}/{widget_id}/rotate")
        return Widget(**data)

    async def get_entitlement(self) -> WidgetEntitlement:
        data = await self._client.get(f"{_BASE}/entitlement")
        return WidgetEntitlement(**data)
