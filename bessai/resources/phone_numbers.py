"""Phone number resource — manage phone numbers and SIP connections."""
from typing import List, Optional

from bessai._client import SyncHTTPClient, AsyncHTTPClient
from bessai.types.phone_number import (
    PhoneNumberResponse,
    PhoneNumberDetailResponse,
    PhoneNumberCreateParams,
    PhoneNumberUpdateParams,
    PhoneNumberAgentUpdateParams,
    SIPConnectionResponse,
    SIPConnectionCreateParams,
    SIPConnectionUpdateParams,
)

_BASE = "/v1/phone-numbers"


class PhoneNumberResource:
    """Synchronous phone number resource.

    Usage::

        client.phone_number.create(phone_number="+905551234567", provider="custom")
        client.phone_number.retrieve("pn_abc123")
        client.phone_number.list()
        client.phone_number.update("pn_abc123", nickname="Main Line")
        client.phone_number.update_agents("pn_abc123", inbound_agent_id="ag_xyz")
        client.phone_number.delete("pn_abc123")

        # SIP connections
        client.phone_number.create_sip_connection("pn_abc123", termination_uri="sip://trunk.example.com:5060")
        client.phone_number.list_sip_connections("pn_abc123")
        client.phone_number.retrieve_sip_connection("pn_abc123", "sc_def456")
        client.phone_number.update_sip_connection("pn_abc123", "sc_def456", transport="TLS")
        client.phone_number.delete_sip_connection("pn_abc123", "sc_def456")
        client.phone_number.sync_sip_connection("pn_abc123", "sc_def456")
    """

    def __init__(self, client: SyncHTTPClient):
        self._client = client

    # ------------------------------------------------------------------
    # Phone Number CRUD
    # ------------------------------------------------------------------

    def create(self, **kwargs) -> PhoneNumberResponse:
        """Register a phone number.

        Args:
            phone_number: Phone number in E.164 format (e.g. "+905551234567").
            nickname: Optional friendly display name.
            provider: Provider type — "custom", "netgsm", "twilio", or "telnyx".
            inbound_agent_id: Agent to handle inbound calls.
            outbound_agent_id: Agent to handle outbound calls.
            allowed_inbound_countries: Country whitelist for inbound (default ["*"]).
            allowed_outbound_countries: Country whitelist for outbound (default ["*"]).
            inbound_webhook_url: Webhook URL for inbound call events.
        """
        body = PhoneNumberCreateParams(**kwargs).to_api_params()
        data = self._client.post(_BASE, json=body)
        return PhoneNumberResponse(**data)

    def retrieve(self, phone_number_id: str) -> PhoneNumberDetailResponse:
        """Get a phone number by ID (includes SIP connections and dispatch rules)."""
        data = self._client.get(f"{_BASE}/{phone_number_id}")
        return PhoneNumberDetailResponse(**data)

    def list(
        self,
        skip: int = 0,
        limit: int = 50,
    ) -> List[PhoneNumberResponse]:
        """List all phone numbers for the organization."""
        data = self._client.get(_BASE, params={"skip": skip, "limit": limit})
        items = data if isinstance(data, list) else data.get("items", [])
        return [PhoneNumberResponse(**p) for p in items]

    def update(self, phone_number_id: str, **kwargs) -> PhoneNumberResponse:
        """Update a phone number's configuration."""
        body = PhoneNumberUpdateParams(**kwargs).to_api_params()
        data = self._client.patch(f"{_BASE}/{phone_number_id}", json=body)
        return PhoneNumberResponse(**data)

    def delete(self, phone_number_id: str) -> None:
        """Delete a phone number and its SIP connections."""
        self._client.delete(f"{_BASE}/{phone_number_id}")

    def update_agents(
        self,
        phone_number_id: str,
        *,
        inbound_agent_id: Optional[str] = None,
        outbound_agent_id: Optional[str] = None,
    ) -> PhoneNumberResponse:
        """Quick-update inbound/outbound agent assignments.

        This also triggers SIP dispatch rule creation when the inbound agent changes.
        """
        body = PhoneNumberAgentUpdateParams(
            inbound_agent_id=inbound_agent_id,
            outbound_agent_id=outbound_agent_id,
        ).to_api_params()
        data = self._client.put(f"{_BASE}/{phone_number_id}/agents", json=body)
        return PhoneNumberResponse(**data)

    # ------------------------------------------------------------------
    # SIP Connections (nested under phone number)
    # ------------------------------------------------------------------

    def create_sip_connection(
        self, phone_number_id: str, **kwargs
    ) -> SIPConnectionResponse:
        """Create a SIP connection and auto-sync to LiveKit.

        Args:
            phone_number_id: Parent phone number ID.
            termination_uri: SIP server URI (e.g. "sip://trunk.example.com:5060").
            username: SIP auth username.
            password: SIP auth password.
            nickname: Friendly name for this connection.
            connection_type: "inbound", "outbound", or "both".
            transport: "TCP", "UDP", or "TLS".
        """
        body = SIPConnectionCreateParams(**kwargs).to_api_params()
        data = self._client.post(
            f"{_BASE}/{phone_number_id}/sip-connections", json=body
        )
        return SIPConnectionResponse(**data)

    def list_sip_connections(
        self, phone_number_id: str
    ) -> List[SIPConnectionResponse]:
        """List all SIP connections for a phone number."""
        data = self._client.get(f"{_BASE}/{phone_number_id}/sip-connections")
        items = data if isinstance(data, list) else data.get("items", [])
        return [SIPConnectionResponse(**c) for c in items]

    def retrieve_sip_connection(
        self, phone_number_id: str, connection_id: str
    ) -> SIPConnectionResponse:
        """Get a single SIP connection by ID."""
        data = self._client.get(
            f"{_BASE}/{phone_number_id}/sip-connections/{connection_id}"
        )
        return SIPConnectionResponse(**data)

    def update_sip_connection(
        self, phone_number_id: str, connection_id: str, **kwargs
    ) -> SIPConnectionResponse:
        """Update a SIP connection and re-sync to LiveKit."""
        body = SIPConnectionUpdateParams(**kwargs).to_api_params()
        data = self._client.patch(
            f"{_BASE}/{phone_number_id}/sip-connections/{connection_id}",
            json=body,
        )
        return SIPConnectionResponse(**data)

    def delete_sip_connection(
        self, phone_number_id: str, connection_id: str
    ) -> None:
        """Delete a SIP connection and clean up LiveKit resources."""
        self._client.delete(
            f"{_BASE}/{phone_number_id}/sip-connections/{connection_id}"
        )

    def sync_sip_connection(
        self, phone_number_id: str, connection_id: str
    ) -> SIPConnectionResponse:
        """Force re-sync a SIP connection with LiveKit."""
        data = self._client.post(
            f"{_BASE}/{phone_number_id}/sip-connections/{connection_id}/sync"
        )
        return SIPConnectionResponse(**data)

    # Backward-compatible aliases
    def get(self, phone_number_id: str) -> PhoneNumberDetailResponse:
        """Alias for :meth:`retrieve`."""
        return self.retrieve(phone_number_id)


class AsyncPhoneNumberResource:
    """Asynchronous phone number resource (mirrors :class:`PhoneNumberResource`)."""

    def __init__(self, client: AsyncHTTPClient):
        self._client = client

    # ------------------------------------------------------------------
    # Phone Number CRUD
    # ------------------------------------------------------------------

    async def create(self, **kwargs) -> PhoneNumberResponse:
        body = PhoneNumberCreateParams(**kwargs).to_api_params()
        data = await self._client.post(_BASE, json=body)
        return PhoneNumberResponse(**data)

    async def retrieve(self, phone_number_id: str) -> PhoneNumberDetailResponse:
        data = await self._client.get(f"{_BASE}/{phone_number_id}")
        return PhoneNumberDetailResponse(**data)

    async def list(
        self,
        skip: int = 0,
        limit: int = 50,
    ) -> List[PhoneNumberResponse]:
        data = await self._client.get(_BASE, params={"skip": skip, "limit": limit})
        items = data if isinstance(data, list) else data.get("items", [])
        return [PhoneNumberResponse(**p) for p in items]

    async def update(self, phone_number_id: str, **kwargs) -> PhoneNumberResponse:
        body = PhoneNumberUpdateParams(**kwargs).to_api_params()
        data = await self._client.patch(f"{_BASE}/{phone_number_id}", json=body)
        return PhoneNumberResponse(**data)

    async def delete(self, phone_number_id: str) -> None:
        await self._client.delete(f"{_BASE}/{phone_number_id}")

    async def update_agents(
        self,
        phone_number_id: str,
        *,
        inbound_agent_id: Optional[str] = None,
        outbound_agent_id: Optional[str] = None,
    ) -> PhoneNumberResponse:
        body = PhoneNumberAgentUpdateParams(
            inbound_agent_id=inbound_agent_id,
            outbound_agent_id=outbound_agent_id,
        ).to_api_params()
        data = await self._client.put(f"{_BASE}/{phone_number_id}/agents", json=body)
        return PhoneNumberResponse(**data)

    # ------------------------------------------------------------------
    # SIP Connections
    # ------------------------------------------------------------------

    async def create_sip_connection(
        self, phone_number_id: str, **kwargs
    ) -> SIPConnectionResponse:
        body = SIPConnectionCreateParams(**kwargs).to_api_params()
        data = await self._client.post(
            f"{_BASE}/{phone_number_id}/sip-connections", json=body
        )
        return SIPConnectionResponse(**data)

    async def list_sip_connections(
        self, phone_number_id: str
    ) -> List[SIPConnectionResponse]:
        data = await self._client.get(f"{_BASE}/{phone_number_id}/sip-connections")
        items = data if isinstance(data, list) else data.get("items", [])
        return [SIPConnectionResponse(**c) for c in items]

    async def retrieve_sip_connection(
        self, phone_number_id: str, connection_id: str
    ) -> SIPConnectionResponse:
        data = await self._client.get(
            f"{_BASE}/{phone_number_id}/sip-connections/{connection_id}"
        )
        return SIPConnectionResponse(**data)

    async def update_sip_connection(
        self, phone_number_id: str, connection_id: str, **kwargs
    ) -> SIPConnectionResponse:
        body = SIPConnectionUpdateParams(**kwargs).to_api_params()
        data = await self._client.patch(
            f"{_BASE}/{phone_number_id}/sip-connections/{connection_id}",
            json=body,
        )
        return SIPConnectionResponse(**data)

    async def delete_sip_connection(
        self, phone_number_id: str, connection_id: str
    ) -> None:
        await self._client.delete(
            f"{_BASE}/{phone_number_id}/sip-connections/{connection_id}"
        )

    async def sync_sip_connection(
        self, phone_number_id: str, connection_id: str
    ) -> SIPConnectionResponse:
        data = await self._client.post(
            f"{_BASE}/{phone_number_id}/sip-connections/{connection_id}/sync"
        )
        return SIPConnectionResponse(**data)

    # Backward-compatible alias
    async def get(self, phone_number_id: str) -> PhoneNumberDetailResponse:
        return await self.retrieve(phone_number_id)


# Backward-compatible aliases
PhoneNumbersResource = PhoneNumberResource
AsyncPhoneNumbersResource = AsyncPhoneNumberResource
