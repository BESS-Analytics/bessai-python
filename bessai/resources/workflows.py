"""
Workflow resource — CRUD, deploy, execute, credentials, agent linking, scheduling.

Function names follow Retell AI SDK conventions for migration compatibility:
  client.workflow.create(json=...)    # Save n8n JSON directly to database
  client.workflow.generate(desc=...) # AI-generate from description
  client.workflow.retrieve(id)
  client.workflow.list()
  client.workflow.update(id, ...)
  client.workflow.delete(id)
  client.workflow.deploy(id)
  client.workflow.execute(id, ...)
  client.workflow.test(id, ...)
  client.workflow.link_agent(id, agent_id, ...)
  client.workflow.set_schedule(id, ...)
"""
from typing import Any, Dict, List, Optional

from bessai._client import SyncHTTPClient, AsyncHTTPClient
from bessai.types.workflow import (
    WorkflowResponse,
    WorkflowDetailResponse,
    WorkflowExecutionResponse,
    WorkflowCreateParams,
    WorkflowCreateResponse,
    WorkflowGenerateParams,
    WorkflowRefineParams,
    WorkflowUpdateParams,
    WorkflowSecretsParams,
    LinkAgentParams,
    UpdateAgentLinkParams,
    ManualExecuteParams,
    GenerateResponse,
    DeployResponse,
    ExecuteResponse,
    CredentialSchemaResponse,
    AgentWorkflowLinkResponse,
    AgentWorkflowListItem,
    ScheduleStatusResponse,
)


class WorkflowResource:
    """Synchronous workflow operations."""

    def __init__(self, client: SyncHTTPClient):
        self._client = client

    # ── CRUD ─────────────────────────────────────────────────────────────

    def create(self, **kwargs) -> WorkflowCreateResponse:
        """Create a workflow by providing n8n JSON directly.

        Saves the workflow_json to the database in draft status.
        Use ``deploy()`` afterwards to push it to n8n.

        Args:
            name: Display name (required).
            trigger_type: post_call, in_call, webhook, or schedule (required).
            workflow_json: Complete n8n workflow JSON dict (required).
            description: What the workflow does.
            trigger_config: Trigger-specific config.
            execution_mode: sync or async (default: async).
            timeout_seconds: Max execution time (1–300).

        Returns:
            Created workflow with ``workflow_id``, ``name``, ``trigger_type``,
            ``status``.
        """
        params = WorkflowCreateParams(**kwargs)
        data = self._client.post("/v1/workflows/", json=params.to_api_params())
        return WorkflowCreateResponse(**data)

    def generate(self, **kwargs) -> GenerateResponse:
        """AI-generate a workflow from a natural-language description.

        Uses AI + n8n-MCP to produce an n8n-compatible workflow JSON.
        For direct JSON save without AI, use ``create()`` instead.

        Args:
            name: Display name (required).
            description: What the workflow should do (required).
            trigger_type: post_call, in_call, webhook, or schedule.
            trigger_config: Optional trigger-specific config.
            agent_id: Optionally link to an agent during generation.

        Returns:
            Generated workflow including ``workflow_id``, ``workflow_json``,
            ``required_secrets``, and ``visualization``.
        """
        params = WorkflowGenerateParams(**kwargs)
        data = self._client.post("/v1/workflows/generate", json=params.to_api_params())
        return GenerateResponse(**data)

    def refine(self, workflow_id: str, **kwargs) -> GenerateResponse:
        """Refine an existing workflow with AI based on feedback.

        Args:
            workflow_id: UUID of the workflow to refine.
            feedback: Natural-language description of what to change.
        """
        params = WorkflowRefineParams(**kwargs)
        data = self._client.post(f"/v1/workflows/{workflow_id}/refine", json=params.to_api_params())
        return GenerateResponse(**data)

    def retrieve(self, workflow_id: str) -> WorkflowDetailResponse:
        """Get a workflow by ID with full detail.

        Args:
            workflow_id: UUID of the workflow.
        """
        data = self._client.get(f"/v1/workflows/{workflow_id}")
        return WorkflowDetailResponse(**data)

    def list(
        self,
        trigger_type: Optional[str] = None,
        status: Optional[str] = None,
        agent_id: Optional[str] = None,
        include_deleted: bool = False,
        page: int = 1,
        per_page: int = 20,
    ) -> List[WorkflowResponse]:
        """List workflows with filtering and pagination.

        Args:
            trigger_type: Filter by post_call, in_call, webhook, schedule.
            status: Filter by draft, active, paused, error.
            agent_id: Filter to workflows linked to this agent.
            include_deleted: Include soft-deleted workflows.
            page: Page number (1-indexed).
            per_page: Items per page (1-100).
        """
        params: Dict[str, Any] = {
            "trigger_type": trigger_type, "status": status,
            "agent_id": agent_id, "include_deleted": include_deleted,
            "page": page, "per_page": per_page,
        }
        data = self._client.get("/v1/workflows", params={k: v for k, v in params.items() if v is not None})
        items = data if isinstance(data, list) else data.get("items", data.get("workflows", []))
        return [WorkflowResponse(**w) for w in items]

    def update(self, workflow_id: str, **kwargs) -> WorkflowDetailResponse:
        """Update workflow settings.

        Only supplied fields are changed.

        Args:
            workflow_id: UUID of the workflow.
            Plus any field from ``WorkflowUpdateParams``.
        """
        params = WorkflowUpdateParams(**kwargs)
        data = self._client.patch(f"/v1/workflows/{workflow_id}", json=params.to_api_params())
        return WorkflowDetailResponse(**data)

    def delete(self, workflow_id: str, hard: bool = False) -> Dict[str, Any]:
        """Delete a workflow (soft-delete by default).

        Soft-deleted workflows can be restored with ``restore()``.
        Use ``hard=True`` for permanent deletion (not recoverable).

        Args:
            workflow_id: UUID of the workflow.
            hard: Permanently delete instead of soft-delete.
        """
        params = {"hard": hard} if hard else None
        return self._client.delete(f"/v1/workflows/{workflow_id}", params=params)

    def restore(self, workflow_id: str) -> Dict[str, Any]:
        """Restore a soft-deleted workflow to draft status.

        Args:
            workflow_id: UUID of the deleted workflow.
        """
        return self._client.post(f"/v1/workflows/{workflow_id}/restore")

    # ── Credentials ──────────────────────────────────────────────────────

    def save_secrets(self, workflow_id: str, **kwargs) -> Dict[str, Any]:
        """Encrypt and save credentials for Runtime Injection.

        Credentials are Fernet-encrypted at rest and only decrypted during
        workflow execution.

        Args:
            workflow_id: UUID of the workflow.
            secrets: List of ``SecretInput`` dicts (key_name, value, type).
            validate_credentials: Test credentials before saving.
        """
        params = WorkflowSecretsParams(**kwargs)
        return self._client.post(f"/v1/workflows/{workflow_id}/secrets", json=params.to_api_params())

    def get_credential_schema(self, credential_type: str) -> CredentialSchemaResponse:
        """Get the required field schema for an n8n credential type.

        Useful for rendering credential input forms.

        Args:
            credential_type: n8n credential type (e.g. ``twilioApi``,
                ``sendGridApi``, ``openAiApi``).
        """
        data = self._client.get(f"/v1/workflows/credential-schema/{credential_type}")
        return CredentialSchemaResponse(**data)

    # ── Deployment & Execution ───────────────────────────────────────────

    def deploy(self, workflow_id: str) -> DeployResponse:
        """Deploy a workflow to n8n and activate it.

        Validates credentials, syncs to n8n, activates the webhook endpoint,
        and marks the workflow as active.

        Args:
            workflow_id: UUID of the workflow.
        """
        data = self._client.post(f"/v1/workflows/{workflow_id}/deploy")
        return DeployResponse(**data)

    def test(self, workflow_id: str, test_data: Optional[Dict[str, Any]] = None) -> ExecuteResponse:
        """Test-execute a workflow with sample call data.

        Args:
            workflow_id: UUID of the workflow.
            test_data: Optional custom test payload (defaults to mock call
                data if omitted).
        """
        body = {"test_data": test_data} if test_data else {}
        data = self._client.post(f"/v1/workflows/{workflow_id}/test", json=body)
        return ExecuteResponse(**data)

    def execute(self, workflow_id: str, **kwargs) -> ExecuteResponse:
        """Manually trigger a workflow execution.

        Args:
            workflow_id: UUID of the workflow.
            context_data: Data payload sent to the workflow.
            execution_mode: ``sync`` or ``async`` (default: async).
        """
        params = ManualExecuteParams(**kwargs)
        data = self._client.post(f"/v1/workflows/{workflow_id}/execute", json=params.to_api_params())
        return ExecuteResponse(**data)

    def list_executions(
        self,
        workflow_id: str,
        status: Optional[str] = None,
        page: int = 1,
        per_page: int = 20,
    ) -> Dict[str, Any]:
        """Get execution history for a workflow.

        Args:
            workflow_id: UUID of the workflow.
            status: Filter by running, success, failed, timeout, skipped.
            page: Page number (1-indexed).
            per_page: Items per page (1-100).

        Returns:
            Dict with ``executions`` list, ``total``, ``page``, ``per_page``.
        """
        params: Dict[str, Any] = {"page": page, "per_page": per_page}
        if status:
            params["status"] = status
        return self._client.get(f"/v1/workflows/{workflow_id}/executions", params=params)

    # ── Import / Export ──────────────────────────────────────────────────

    def export(self, workflow_id: str) -> Dict[str, Any]:
        """Export a workflow as a portable JSON object.

        Excludes secrets and org-specific IDs.

        Args:
            workflow_id: UUID of the workflow.
        """
        return self._client.get(f"/v1/workflows/{workflow_id}/export")

    def import_workflow(self, file_path: str) -> Dict[str, Any]:
        """Import a workflow from a previously exported JSON file.

        Creates the workflow in draft status. Credentials must be
        configured separately after import.

        Args:
            file_path: Local path to the workflow JSON file.

        Returns:
            Dict with ``workflow_id``, ``workflow_name``, ``warnings``.
        """
        with open(file_path, "rb") as f:
            return self._client.post(
                "/v1/workflows/import",
                files={"file": ("workflow.json", f, "application/json")},
            )

    # ── Agent Linking ────────────────────────────────────────────────────

    def link_agent(self, workflow_id: str, agent_id: str, **kwargs) -> AgentWorkflowLinkResponse:
        """Link a workflow to an agent with optional trigger conditions.

        Args:
            workflow_id: UUID of the workflow.
            agent_id: UUID of the agent.
            trigger_condition_description: Natural-language condition
                evaluated by the LLM at runtime.
            priority: Execution order (higher = runs first).
            execution_mode_override: Force sync or async.
        """
        params = LinkAgentParams(**kwargs)
        data = self._client.post(
            f"/v1/workflows/{workflow_id}/agents/{agent_id}",
            json=params.to_api_params(),
        )
        return AgentWorkflowLinkResponse(**data)

    def update_agent_link(self, workflow_id: str, agent_id: str, **kwargs) -> AgentWorkflowLinkResponse:
        """Update an agent-workflow link's configuration.

        Args:
            workflow_id: UUID of the workflow.
            agent_id: UUID of the agent.
            trigger_condition_description: New trigger condition.
            priority: New priority.
            is_enabled: Enable or disable the link.
            execution_mode_override: Change execution mode.
        """
        params = UpdateAgentLinkParams(**kwargs)
        data = self._client.patch(
            f"/v1/workflows/{workflow_id}/agents/{agent_id}",
            json=params.to_api_params(),
        )
        return AgentWorkflowLinkResponse(**data)

    def unlink_agent(self, workflow_id: str, agent_id: str) -> Dict[str, Any]:
        """Remove a workflow-agent link.

        Args:
            workflow_id: UUID of the workflow.
            agent_id: UUID of the agent.
        """
        return self._client.delete(f"/v1/workflows/{workflow_id}/agents/{agent_id}")

    def list_agents(self, workflow_id: str) -> List[AgentWorkflowLinkResponse]:
        """Get all agents linked to a workflow.

        Args:
            workflow_id: UUID of the workflow.
        """
        data = self._client.get(f"/v1/workflows/{workflow_id}/agents")
        items = data.get("agents", []) if isinstance(data, dict) else data
        return [AgentWorkflowLinkResponse(**a) for a in items]

    def list_by_agent(self, agent_id: str) -> List[AgentWorkflowListItem]:
        """Get all workflows linked to an agent.

        Args:
            agent_id: UUID of the agent.
        """
        data = self._client.get(f"/v1/workflows/by-agent/{agent_id}")
        items = data.get("workflows", []) if isinstance(data, dict) else data
        return [AgentWorkflowListItem(**w) for w in items]

    # ── Scheduling ───────────────────────────────────────────────────────

    def set_schedule(
        self,
        workflow_id: str,
        cron: Optional[str] = None,
        interval_minutes: Optional[int] = None,
        timezone: str = "UTC",
    ) -> Dict[str, Any]:
        """Set or update a workflow's schedule.

        The workflow's trigger_type must be ``schedule``.

        Args:
            workflow_id: UUID of the workflow.
            cron: Cron expression (e.g. ``0 9 * * *`` for 9 AM daily).
            interval_minutes: Run every N minutes (alternative to cron).
            timezone: Timezone for cron (default: UTC).
        """
        params: Dict[str, Any] = {"timezone": timezone}
        if cron:
            params["cron"] = cron
        if interval_minutes:
            params["interval_minutes"] = interval_minutes
        return self._client.post(f"/v1/workflows/{workflow_id}/schedule", params=params)

    def remove_schedule(self, workflow_id: str) -> Dict[str, Any]:
        """Remove a workflow from the schedule.

        Args:
            workflow_id: UUID of the workflow.
        """
        return self._client.delete(f"/v1/workflows/{workflow_id}/schedule")

    def get_schedule(self, workflow_id: str) -> ScheduleStatusResponse:
        """Get a workflow's current schedule status.

        Args:
            workflow_id: UUID of the workflow.
        """
        data = self._client.get(f"/v1/workflows/{workflow_id}/schedule")
        return ScheduleStatusResponse(**data)

    def list_schedules(self) -> Dict[str, Any]:
        """List all currently scheduled workflows.

        Returns:
            Dict with ``total`` and ``scheduled_workflows`` list.
        """
        return self._client.get("/v1/workflows/schedules/all")


# =============================================================================
# Async variant
# =============================================================================


class AsyncWorkflowResource:
    """Asynchronous workflow operations."""

    def __init__(self, client: AsyncHTTPClient):
        self._client = client

    # ── CRUD ─────────────────────────────────────────────────────────────

    async def create(self, **kwargs) -> WorkflowCreateResponse:
        """Create a workflow by providing n8n JSON directly."""
        params = WorkflowCreateParams(**kwargs)
        data = await self._client.post("/v1/workflows/", json=params.to_api_params())
        return WorkflowCreateResponse(**data)

    async def generate(self, **kwargs) -> GenerateResponse:
        """AI-generate a workflow from a natural-language description."""
        params = WorkflowGenerateParams(**kwargs)
        data = await self._client.post("/v1/workflows/generate", json=params.to_api_params())
        return GenerateResponse(**data)

    async def refine(self, workflow_id: str, **kwargs) -> GenerateResponse:
        """Refine an existing workflow with AI based on feedback."""
        params = WorkflowRefineParams(**kwargs)
        data = await self._client.post(f"/v1/workflows/{workflow_id}/refine", json=params.to_api_params())
        return GenerateResponse(**data)

    async def retrieve(self, workflow_id: str) -> WorkflowDetailResponse:
        """Get a workflow by ID with full detail."""
        data = await self._client.get(f"/v1/workflows/{workflow_id}")
        return WorkflowDetailResponse(**data)

    async def list(
        self,
        trigger_type: Optional[str] = None,
        status: Optional[str] = None,
        agent_id: Optional[str] = None,
        include_deleted: bool = False,
        page: int = 1,
        per_page: int = 20,
    ) -> List[WorkflowResponse]:
        """List workflows with filtering and pagination."""
        params: Dict[str, Any] = {
            "trigger_type": trigger_type, "status": status,
            "agent_id": agent_id, "include_deleted": include_deleted,
            "page": page, "per_page": per_page,
        }
        data = await self._client.get("/v1/workflows", params={k: v for k, v in params.items() if v is not None})
        items = data if isinstance(data, list) else data.get("items", data.get("workflows", []))
        return [WorkflowResponse(**w) for w in items]

    async def update(self, workflow_id: str, **kwargs) -> WorkflowDetailResponse:
        """Update workflow settings."""
        params = WorkflowUpdateParams(**kwargs)
        data = await self._client.patch(f"/v1/workflows/{workflow_id}", json=params.to_api_params())
        return WorkflowDetailResponse(**data)

    async def delete(self, workflow_id: str, hard: bool = False) -> Dict[str, Any]:
        """Delete a workflow (soft-delete by default)."""
        params = {"hard": hard} if hard else None
        return await self._client.delete(f"/v1/workflows/{workflow_id}", params=params)

    async def restore(self, workflow_id: str) -> Dict[str, Any]:
        """Restore a soft-deleted workflow to draft status."""
        return await self._client.post(f"/v1/workflows/{workflow_id}/restore")

    # ── Credentials ──────────────────────────────────────────────────────

    async def save_secrets(self, workflow_id: str, **kwargs) -> Dict[str, Any]:
        """Encrypt and save credentials for Runtime Injection."""
        params = WorkflowSecretsParams(**kwargs)
        return await self._client.post(f"/v1/workflows/{workflow_id}/secrets", json=params.to_api_params())

    async def get_credential_schema(self, credential_type: str) -> CredentialSchemaResponse:
        """Get the required field schema for an n8n credential type."""
        data = await self._client.get(f"/v1/workflows/credential-schema/{credential_type}")
        return CredentialSchemaResponse(**data)

    # ── Deployment & Execution ───────────────────────────────────────────

    async def deploy(self, workflow_id: str) -> DeployResponse:
        """Deploy a workflow to n8n and activate it."""
        data = await self._client.post(f"/v1/workflows/{workflow_id}/deploy")
        return DeployResponse(**data)

    async def test(self, workflow_id: str, test_data: Optional[Dict[str, Any]] = None) -> ExecuteResponse:
        """Test-execute a workflow with sample call data."""
        body = {"test_data": test_data} if test_data else {}
        data = await self._client.post(f"/v1/workflows/{workflow_id}/test", json=body)
        return ExecuteResponse(**data)

    async def execute(self, workflow_id: str, **kwargs) -> ExecuteResponse:
        """Manually trigger a workflow execution."""
        params = ManualExecuteParams(**kwargs)
        data = await self._client.post(f"/v1/workflows/{workflow_id}/execute", json=params.to_api_params())
        return ExecuteResponse(**data)

    async def list_executions(
        self,
        workflow_id: str,
        status: Optional[str] = None,
        page: int = 1,
        per_page: int = 20,
    ) -> Dict[str, Any]:
        """Get execution history for a workflow."""
        params: Dict[str, Any] = {"page": page, "per_page": per_page}
        if status:
            params["status"] = status
        return await self._client.get(f"/v1/workflows/{workflow_id}/executions", params=params)

    # ── Import / Export ──────────────────────────────────────────────────

    async def export(self, workflow_id: str) -> Dict[str, Any]:
        """Export a workflow as a portable JSON object."""
        return await self._client.get(f"/v1/workflows/{workflow_id}/export")

    async def import_workflow(self, file_path: str) -> Dict[str, Any]:
        """Import a workflow from a previously exported JSON file."""
        with open(file_path, "rb") as f:
            return await self._client.post(
                "/v1/workflows/import",
                files={"file": ("workflow.json", f, "application/json")},
            )

    # ── Agent Linking ────────────────────────────────────────────────────

    async def link_agent(self, workflow_id: str, agent_id: str, **kwargs) -> AgentWorkflowLinkResponse:
        """Link a workflow to an agent with optional trigger conditions."""
        params = LinkAgentParams(**kwargs)
        data = await self._client.post(
            f"/v1/workflows/{workflow_id}/agents/{agent_id}",
            json=params.to_api_params(),
        )
        return AgentWorkflowLinkResponse(**data)

    async def update_agent_link(self, workflow_id: str, agent_id: str, **kwargs) -> AgentWorkflowLinkResponse:
        """Update an agent-workflow link's configuration."""
        params = UpdateAgentLinkParams(**kwargs)
        data = await self._client.patch(
            f"/v1/workflows/{workflow_id}/agents/{agent_id}",
            json=params.to_api_params(),
        )
        return AgentWorkflowLinkResponse(**data)

    async def unlink_agent(self, workflow_id: str, agent_id: str) -> Dict[str, Any]:
        """Remove a workflow-agent link."""
        return await self._client.delete(f"/v1/workflows/{workflow_id}/agents/{agent_id}")

    async def list_agents(self, workflow_id: str) -> List[AgentWorkflowLinkResponse]:
        """Get all agents linked to a workflow."""
        data = await self._client.get(f"/v1/workflows/{workflow_id}/agents")
        items = data.get("agents", []) if isinstance(data, dict) else data
        return [AgentWorkflowLinkResponse(**a) for a in items]

    async def list_by_agent(self, agent_id: str) -> List[AgentWorkflowListItem]:
        """Get all workflows linked to an agent."""
        data = await self._client.get(f"/v1/workflows/by-agent/{agent_id}")
        items = data.get("workflows", []) if isinstance(data, dict) else data
        return [AgentWorkflowListItem(**w) for w in items]

    # ── Scheduling ───────────────────────────────────────────────────────

    async def set_schedule(
        self,
        workflow_id: str,
        cron: Optional[str] = None,
        interval_minutes: Optional[int] = None,
        timezone: str = "UTC",
    ) -> Dict[str, Any]:
        """Set or update a workflow's schedule."""
        params: Dict[str, Any] = {"timezone": timezone}
        if cron:
            params["cron"] = cron
        if interval_minutes:
            params["interval_minutes"] = interval_minutes
        return await self._client.post(f"/v1/workflows/{workflow_id}/schedule", params=params)

    async def remove_schedule(self, workflow_id: str) -> Dict[str, Any]:
        """Remove a workflow from the schedule."""
        return await self._client.delete(f"/v1/workflows/{workflow_id}/schedule")

    async def get_schedule(self, workflow_id: str) -> ScheduleStatusResponse:
        """Get a workflow's current schedule status."""
        data = await self._client.get(f"/v1/workflows/{workflow_id}/schedule")
        return ScheduleStatusResponse(**data)

    async def list_schedules(self) -> Dict[str, Any]:
        """List all currently scheduled workflows."""
        return await self._client.get("/v1/workflows/schedules/all")


# Backward-compatible aliases
WorkflowsResource = WorkflowResource
AsyncWorkflowsResource = AsyncWorkflowResource
