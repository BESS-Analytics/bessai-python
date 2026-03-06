"""
Agent resource — CRUD, publish, versioning, export/import.

Function names follow Retell AI SDK conventions for migration compatibility:
  client.agent.create()
  client.agent.retrieve(agent_id)
  client.agent.update(agent_id, ...)
  client.agent.list()
  client.agent.delete(agent_id)
  client.agent.publish(agent_id)
  client.agent.get_versions(agent_id)
  client.agent.export(agent_id)
  client.agent.import_agent(file_path)
"""
from typing import Any, Dict, List, Optional

from bessai._client import SyncHTTPClient, AsyncHTTPClient
from bessai.types.agent import (
    AgentResponse,
    AgentCreateParams,
    AgentUpdateParams,
    AgentVersion,
)


class AgentResource:
    """Synchronous agent operations."""

    def __init__(self, client: SyncHTTPClient):
        self._client = client

    def create(self, **kwargs) -> AgentResponse:
        """Create a new voice AI agent.

        The agent is created in draft state. Call ``publish()`` to make it
        callable.

        Args:
            agent_name: Display name (required).
            voice_id: Voice identifier (required).
            Plus any field from ``AgentCreateParams``.

        Returns:
            The newly created agent with its first version.
        """
        params = AgentCreateParams(**kwargs)
        body = params.to_api_params()
        data = self._client.post("/v1/agents", json=body)
        return AgentResponse(**data)

    def retrieve(self, agent_id: str) -> AgentResponse:
        """Get an agent by ID, including all version history.

        Args:
            agent_id: UUID of the agent.
        """
        data = self._client.get(f"/v1/agents/{agent_id}")
        return AgentResponse(**data)

    def list(self, skip: int = 0, limit: int = 20) -> List[AgentResponse]:
        """List all agents for the current organization.

        Args:
            skip: Pagination offset (default 0).
            limit: Page size, 1-100 (default 20).
        """
        data = self._client.get("/v1/agents", params={"skip": skip, "limit": limit})
        if isinstance(data, list):
            return [AgentResponse(**a) for a in data]
        return [AgentResponse(**a) for a in data.get("items", [])]

    def update(self, agent_id: str, **kwargs) -> AgentResponse:
        """Update agent configuration.

        Only supplied fields are changed.  Changes are saved as a new draft
        version.  Call ``publish()`` to make them live.

        Args:
            agent_id: UUID of the agent to update.
            Plus any field from ``AgentUpdateParams``.
        """
        params = AgentUpdateParams(**kwargs)
        body = params.to_api_params()
        data = self._client.patch(f"/v1/agents/{agent_id}", json=body)
        return AgentResponse(**data)

    def delete(self, agent_id: str) -> None:
        """Permanently delete an agent and all its versions.

        Args:
            agent_id: UUID of the agent.
        """
        self._client.delete(f"/v1/agents/{agent_id}")

    def publish(self, agent_id: str) -> AgentResponse:
        """Publish the current draft as a new live version.

        Only published agents can receive phone/web calls.

        Args:
            agent_id: UUID of the agent.
        """
        data = self._client.post(f"/v1/agents/{agent_id}/publish")
        return AgentResponse(**data)

    def get_versions(self, agent_id: str) -> List[AgentVersion]:
        """Get the full version history of an agent.

        Args:
            agent_id: UUID of the agent.
        """
        data = self._client.get(f"/v1/agents/{agent_id}/versions")
        return [AgentVersion(**v) for v in data]

    def export(self, agent_id: str) -> Dict[str, Any]:
        """Export an agent as a portable JSON object.

        Args:
            agent_id: UUID of the agent.

        Returns:
            JSON-serializable dict with agent configuration.
        """
        return self._client.get(f"/v1/agents/{agent_id}/export")

    def import_agent(self, file_path: str) -> AgentResponse:
        """Import an agent from a previously exported JSON file.

        Args:
            file_path: Local path to the agent JSON file.

        Returns:
            The newly created agent.
        """
        with open(file_path, "rb") as f:
            data = self._client.post(
                "/v1/agents/import",
                files={"file": ("agent.json", f, "application/json")},
            )
        return AgentResponse(**data)


class AsyncAgentResource:
    """Asynchronous agent operations."""

    def __init__(self, client: AsyncHTTPClient):
        self._client = client

    async def create(self, **kwargs) -> AgentResponse:
        """Create a new voice AI agent."""
        params = AgentCreateParams(**kwargs)
        body = params.to_api_params()
        data = await self._client.post("/v1/agents", json=body)
        return AgentResponse(**data)

    async def retrieve(self, agent_id: str) -> AgentResponse:
        """Get an agent by ID."""
        data = await self._client.get(f"/v1/agents/{agent_id}")
        return AgentResponse(**data)

    async def list(self, skip: int = 0, limit: int = 20) -> List[AgentResponse]:
        """List all agents for the current organization."""
        data = await self._client.get("/v1/agents", params={"skip": skip, "limit": limit})
        if isinstance(data, list):
            return [AgentResponse(**a) for a in data]
        return [AgentResponse(**a) for a in data.get("items", [])]

    async def update(self, agent_id: str, **kwargs) -> AgentResponse:
        """Update agent configuration."""
        params = AgentUpdateParams(**kwargs)
        body = params.to_api_params()
        data = await self._client.patch(f"/v1/agents/{agent_id}", json=body)
        return AgentResponse(**data)

    async def delete(self, agent_id: str) -> None:
        """Permanently delete an agent and all its versions."""
        await self._client.delete(f"/v1/agents/{agent_id}")

    async def publish(self, agent_id: str) -> AgentResponse:
        """Publish the current draft as a new live version."""
        data = await self._client.post(f"/v1/agents/{agent_id}/publish")
        return AgentResponse(**data)

    async def get_versions(self, agent_id: str) -> List[AgentVersion]:
        """Get version history."""
        data = await self._client.get(f"/v1/agents/{agent_id}/versions")
        return [AgentVersion(**v) for v in data]

    async def export(self, agent_id: str) -> Dict[str, Any]:
        """Export an agent as JSON."""
        return await self._client.get(f"/v1/agents/{agent_id}/export")

    async def import_agent(self, file_path: str) -> AgentResponse:
        """Import an agent from JSON file."""
        with open(file_path, "rb") as f:
            data = await self._client.post(
                "/v1/agents/import",
                files={"file": ("agent.json", f, "application/json")},
            )
        return AgentResponse(**data)
