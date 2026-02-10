"""Agents resource — CRUD + publish + versions."""
from typing import List, Optional

from bessai._client import SyncHTTPClient, AsyncHTTPClient
from bessai.types.agent import Agent, AgentCreate, AgentUpdate, AgentVersion


class AgentsResource:
    """Sync agents resource."""

    def __init__(self, client: SyncHTTPClient):
        self._client = client

    def create(self, **kwargs) -> Agent:
        """Create a new voice AI agent."""
        body = AgentCreate(**kwargs).model_dump(exclude_none=True)
        data = self._client.post("/v1/agents", json=body)
        return Agent(**data)

    def list(self, skip: int = 0, limit: int = 20) -> List[Agent]:
        """List all agents."""
        data = self._client.get("/v1/agents", params={"skip": skip, "limit": limit})
        if isinstance(data, list):
            return [Agent(**a) for a in data]
        return [Agent(**a) for a in data.get("items", data if isinstance(data, list) else [])]

    def get(self, agent_id: str) -> Agent:
        """Get agent by ID."""
        data = self._client.get(f"/v1/agents/{agent_id}")
        return Agent(**data)

    def update(self, agent_id: str, **kwargs) -> Agent:
        """Update agent configuration."""
        body = AgentUpdate(**kwargs).model_dump(exclude_none=True)
        data = self._client.patch(f"/v1/agents/{agent_id}", json=body)
        return Agent(**data)

    def delete(self, agent_id: str) -> None:
        """Delete an agent."""
        self._client.delete(f"/v1/agents/{agent_id}")

    def publish(self, agent_id: str) -> Agent:
        """Publish current draft as a new version."""
        data = self._client.post(f"/v1/agents/{agent_id}/publish")
        return Agent(**data)

    def list_versions(self, agent_id: str) -> List[AgentVersion]:
        """Get version history for an agent."""
        data = self._client.get(f"/v1/agents/{agent_id}/versions")
        return [AgentVersion(**v) for v in data]


class AsyncAgentsResource:
    """Async agents resource."""

    def __init__(self, client: AsyncHTTPClient):
        self._client = client

    async def create(self, **kwargs) -> Agent:
        body = AgentCreate(**kwargs).model_dump(exclude_none=True)
        data = await self._client.post("/v1/agents", json=body)
        return Agent(**data)

    async def list(self, skip: int = 0, limit: int = 20) -> List[Agent]:
        data = await self._client.get("/v1/agents", params={"skip": skip, "limit": limit})
        if isinstance(data, list):
            return [Agent(**a) for a in data]
        return [Agent(**a) for a in data.get("items", data if isinstance(data, list) else [])]

    async def get(self, agent_id: str) -> Agent:
        data = await self._client.get(f"/v1/agents/{agent_id}")
        return Agent(**data)

    async def update(self, agent_id: str, **kwargs) -> Agent:
        body = AgentUpdate(**kwargs).model_dump(exclude_none=True)
        data = await self._client.patch(f"/v1/agents/{agent_id}", json=body)
        return Agent(**data)

    async def delete(self, agent_id: str) -> None:
        await self._client.delete(f"/v1/agents/{agent_id}")

    async def publish(self, agent_id: str) -> Agent:
        data = await self._client.post(f"/v1/agents/{agent_id}/publish")
        return Agent(**data)

    async def list_versions(self, agent_id: str) -> List[AgentVersion]:
        data = await self._client.get(f"/v1/agents/{agent_id}/versions")
        return [AgentVersion(**v) for v in data]
