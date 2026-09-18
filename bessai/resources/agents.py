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
from bessai.types.workflow import (
    AgentWorkflowLinkResponse,
    AgentWorkflowListItem,
    LinkAgentParams,
    UpdateAgentLinkParams,
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

    def retrieve(self, agent_id: str, versions: Optional[str] = None) -> AgentResponse:
        """Get an agent by ID, including its version history.

        ``versions`` comes back **newest first**: ``agent.versions[0]`` is the
        current configuration and its ``version`` number is the one to quote
        back to a user ("you are editing version 41").

        Args:
            agent_id: UUID of the agent.
            versions: How much history to fetch — ``"all"`` (server default,
                every version), ``"latest"`` (only the current one, still at
                index 0) or ``"none"``. Agents accumulate a version per publish
                and each carries its own full system prompt, so pass
                ``"latest"`` when you only need the live config.
                ``agent.version_count`` still reports the true total in every
                mode — never count ``len(agent.versions)`` instead.
        """
        params = {"versions": versions} if versions else None
        data = self._client.get(f"/v1/agents/{agent_id}", params=params)
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

        Only supplied fields are changed. The change is written **in place** to
        the agent's current (highest-numbered) version — it does not create a
        separate draft. On an agent that has already been published, that is the
        published version, so **outbound** calls use the new configuration
        immediately, while **inbound** calls keep answering with the last
        published snapshot until you call ``publish()``.

        Call ``publish()`` after updating to put both directions on the same
        configuration and keep the previous one as history.

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

    # ── Workflow Linking (convenience wrappers) ──────────────────────────

    def link_workflow(self, agent_id: str, workflow_id: str, **kwargs) -> AgentWorkflowLinkResponse:
        """Link a workflow to this agent.

        Convenience method — delegates to the workflow linking endpoint.

        Args:
            agent_id: UUID of the agent.
            workflow_id: UUID of the workflow.
            trigger_condition_description: Natural-language trigger condition.
            priority: Execution order (higher = runs first).
            execution_mode_override: Force sync or async.
        """
        params = LinkAgentParams(**kwargs)
        data = self._client.post(
            f"/v1/workflows/{workflow_id}/agents/{agent_id}",
            json=params.to_api_params(),
        )
        return AgentWorkflowLinkResponse(**data)

    def unlink_workflow(self, agent_id: str, workflow_id: str) -> Dict[str, Any]:
        """Remove a workflow link from this agent.

        Args:
            agent_id: UUID of the agent.
            workflow_id: UUID of the workflow.
        """
        return self._client.delete(f"/v1/workflows/{workflow_id}/agents/{agent_id}")

    def list_workflows(self, agent_id: str) -> List[AgentWorkflowListItem]:
        """Get all workflows linked to an agent.

        Args:
            agent_id: UUID of the agent.
        """
        data = self._client.get(f"/v1/workflows/by-agent/{agent_id}")
        items = data.get("workflows", []) if isinstance(data, dict) else data
        return [AgentWorkflowListItem(**w) for w in items]


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

    async def retrieve(self, agent_id: str, versions: Optional[str] = None) -> AgentResponse:
        """Get an agent by ID, including its version history.

        ``versions`` comes back newest first — ``agent.versions[0]`` is the
        current configuration and its ``version`` number is the one to quote
        back to a user. Pass ``versions="latest"`` (or ``"none"``) to skip the
        older versions, each of which carries its own full system prompt.
        """
        params = {"versions": versions} if versions else None
        data = await self._client.get(f"/v1/agents/{agent_id}", params=params)
        return AgentResponse(**data)

    async def list(self, skip: int = 0, limit: int = 20) -> List[AgentResponse]:
        """List all agents for the current organization."""
        data = await self._client.get("/v1/agents", params={"skip": skip, "limit": limit})
        if isinstance(data, list):
            return [AgentResponse(**a) for a in data]
        return [AgentResponse(**a) for a in data.get("items", [])]

    async def update(self, agent_id: str, **kwargs) -> AgentResponse:
        """Update agent configuration.

        Writes in place to the agent's current (highest-numbered) version — not
        a draft copy. On a published agent, outbound calls pick the change up
        immediately; inbound calls keep the last published snapshot until
        ``publish()``.
        """
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

    # ── Workflow Linking (convenience wrappers) ──────────────────────────

    async def link_workflow(self, agent_id: str, workflow_id: str, **kwargs) -> AgentWorkflowLinkResponse:
        """Link a workflow to this agent."""
        params = LinkAgentParams(**kwargs)
        data = await self._client.post(
            f"/v1/workflows/{workflow_id}/agents/{agent_id}",
            json=params.to_api_params(),
        )
        return AgentWorkflowLinkResponse(**data)

    async def unlink_workflow(self, agent_id: str, workflow_id: str) -> Dict[str, Any]:
        """Remove a workflow link from this agent."""
        return await self._client.delete(f"/v1/workflows/{workflow_id}/agents/{agent_id}")

    async def list_workflows(self, agent_id: str) -> List[AgentWorkflowListItem]:
        """Get all workflows linked to an agent."""
        data = await self._client.get(f"/v1/workflows/by-agent/{agent_id}")
        items = data.get("workflows", []) if isinstance(data, dict) else data
        return [AgentWorkflowListItem(**w) for w in items]
