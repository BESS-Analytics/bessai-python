"""Workflow types for the BESS AI SDK.

Workflows are n8n-compatible automation definitions that can be linked to
agents and triggered by calls, webhooks, or schedules.

Trigger types:
  - ``post_call``  — Runs after a call ends (async).
  - ``in_call``    — Runs during a call (sync, < 4 s timeout).
  - ``webhook``    — Triggered by an external HTTP POST.
  - ``schedule``   — Runs on a cron or interval schedule.
"""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# =============================================================================
# Response Models
# =============================================================================


class WorkflowResponse(BaseModel):
    """Workflow returned by the API (list context)."""
    workflow_id: str = Field(alias="id")
    name: Optional[str] = None
    description: Optional[str] = None
    trigger_type: Optional[str] = Field(None, description="post_call, in_call, webhook, schedule")
    status: Optional[str] = Field(None, description="draft, active, paused, error")
    is_active: Optional[bool] = None
    execution_mode: Optional[str] = Field(None, description="sync or async")
    timeout_seconds: Optional[int] = None
    n8n_workflow_id: Optional[str] = None
    webhook_slug: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    deployed_at: Optional[str] = None
    last_executed_at: Optional[str] = None

    class Config:
        populate_by_name = True


class WorkflowDetailResponse(BaseModel):
    """Workflow returned by the retrieve endpoint (full detail)."""
    workflow_id: str = Field(alias="id")
    name: Optional[str] = None
    description: Optional[str] = None
    trigger_type: Optional[str] = None
    trigger_config: Optional[Dict[str, Any]] = None
    status: Optional[str] = None
    is_active: Optional[bool] = None
    execution_mode: Optional[str] = None
    timeout_seconds: Optional[int] = None
    workflow_json: Optional[Dict[str, Any]] = None
    n8n_workflow_id: Optional[str] = None
    webhook_slug: Optional[str] = None
    detected_credentials: Optional[List[Dict[str, Any]]] = None
    original_description: Optional[str] = None
    generation_history: Optional[List[Dict[str, Any]]] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    deployed_at: Optional[str] = None
    last_executed_at: Optional[str] = None

    class Config:
        populate_by_name = True


class WorkflowExecutionResponse(BaseModel):
    """A single workflow execution record."""
    execution_id: str = Field(alias="id")
    workflow_id: Optional[str] = None
    call_id: Optional[str] = None
    trigger_type: Optional[str] = None
    trigger_source: Optional[str] = Field(None, description="post_call_worker, voice_agent, external, scheduler, manual")
    n8n_execution_id: Optional[str] = None
    status: str = Field(description="running, success, failed, timeout, skipped")
    input_snapshot: Optional[Dict[str, Any]] = None
    output_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    error_stack: Optional[str] = None
    execution_time_ms: Optional[int] = None
    retry_count: Optional[int] = None
    is_retry: Optional[bool] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None

    class Config:
        populate_by_name = True


class CredentialFieldSchema(BaseModel):
    """A single field in a credential type's schema."""
    name: str
    required: bool = True
    type: str = "string"
    description: Optional[str] = None
    default: Optional[Any] = None


class CredentialSchemaResponse(BaseModel):
    """Schema describing the required fields for an n8n credential type."""
    credential_type: str
    fields: List[CredentialFieldSchema] = []
    source: Optional[str] = Field(None, description="known_schema, n8n_api, or fallback")


class AgentWorkflowLinkResponse(BaseModel):
    """A link between an agent and a workflow."""
    agent_id: str
    workflow_id: str
    trigger_condition_description: Optional[str] = Field(
        None, description="Natural-language condition evaluated by the LLM at runtime.")
    priority: int = Field(0, description="Higher values run first when multiple workflows match.")
    is_enabled: bool = True
    execution_mode_override: Optional[str] = Field(None, description="Override workflow's default sync/async.")


class AgentWorkflowListItem(BaseModel):
    """Workflow details enriched with link config (returned by list-by-agent)."""
    workflow_id: str = Field(alias="id")
    name: Optional[str] = None
    description: Optional[str] = None
    trigger_type: Optional[str] = None
    status: Optional[str] = None
    is_active: Optional[bool] = None
    trigger_condition_description: Optional[str] = None
    priority: int = 0
    is_enabled: bool = True
    execution_mode_override: Optional[str] = None

    class Config:
        populate_by_name = True


class ScheduleStatusResponse(BaseModel):
    """Current schedule status for a workflow."""
    workflow_id: str
    is_scheduled: bool = False
    trigger_type: Optional[str] = None
    trigger_config: Optional[Dict[str, Any]] = None
    next_run: Optional[str] = None
    job_details: Optional[Dict[str, Any]] = None


class WorkflowCreateResponse(BaseModel):
    """Result of creating a workflow via direct JSON save."""
    workflow_id: str
    name: str
    trigger_type: Optional[str] = None
    status: Optional[str] = None
    message: Optional[str] = None


class GenerateResponse(BaseModel):
    """Result of AI workflow generation."""
    workflow_id: Optional[str] = None
    workflow_json: Optional[Dict[str, Any]] = None
    required_secrets: Optional[List[Dict[str, Any]]] = None
    visualization: Optional[Dict[str, Any]] = None


class DeployResponse(BaseModel):
    """Result of deploying a workflow to n8n."""
    status: str
    workflow_id: Optional[str] = None
    n8n_workflow_id: Optional[str] = None
    error: Optional[str] = None


class ExecuteResponse(BaseModel):
    """Result of triggering a workflow execution."""
    status: str
    execution_id: Optional[str] = None
    execution_time_ms: Optional[int] = None
    output: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


# =============================================================================
# Request Models
# =============================================================================


class WorkflowCreateParams(BaseModel):
    """Parameters for creating a workflow with direct n8n JSON."""
    name: str = Field(..., min_length=1, max_length=255,
                      description="Display name for the workflow.")
    description: Optional[str] = Field(None,
                                       description="What the workflow does.")
    trigger_type: str = Field("post_call",
                              description="post_call, in_call, webhook, or schedule.")
    workflow_json: Dict[str, Any] = Field(...,
                                          description="Complete n8n workflow JSON.")
    trigger_config: Optional[Dict[str, Any]] = Field(None,
                                                     description="Trigger-specific config.")
    execution_mode: Optional[str] = Field(None, description="sync or async.")
    timeout_seconds: Optional[int] = Field(None, ge=1, le=300)

    def to_api_params(self) -> dict:
        return self.model_dump(exclude_none=True)


class WorkflowGenerateParams(BaseModel):
    """Parameters for AI-generating a workflow from natural language."""
    name: str = Field(..., min_length=1, max_length=255,
                      description="Display name for the workflow.")
    description: str = Field(..., min_length=1,
                             description="Natural-language description of what the workflow should do.")
    trigger_type: str = Field("post_call",
                              description="post_call, in_call, webhook, or schedule.")
    trigger_config: Optional[Dict[str, Any]] = Field(None,
                                                     description="Trigger-specific config (cron, webhook slug, event filters).")
    agent_id: Optional[str] = Field(None,
                                    description="Optionally link to an agent during generation.")

    def to_api_params(self) -> dict:
        return self.model_dump(exclude_none=True)


class WorkflowRefineParams(BaseModel):
    """Parameters for refining an existing workflow with AI."""
    feedback: str = Field(..., min_length=1,
                          description="Natural-language description of what to change.")

    def to_api_params(self) -> dict:
        return self.model_dump(exclude_none=True)


class WorkflowUpdateParams(BaseModel):
    """Parameters for updating a workflow's settings."""
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    is_active: Optional[bool] = None
    status: Optional[str] = Field(None, description="draft, active, paused")
    execution_mode: Optional[str] = Field(None, description="sync or async")
    timeout_seconds: Optional[int] = Field(None, ge=1, le=300)

    def to_api_params(self) -> dict:
        return self.model_dump(exclude_none=True)


class SecretInput(BaseModel):
    """A single credential entry to save."""
    key_name: str = Field(..., description="Credential identifier (maps to n8n credential type).")
    value: str = Field(..., description="The secret value (will be Fernet-encrypted at rest).")
    type: str = Field("string", description="string, pem, json, or oauth.")


class WorkflowSecretsParams(BaseModel):
    """Parameters for saving workflow credentials."""
    secrets: List[SecretInput] = Field(..., min_items=1)
    validate_credentials: bool = Field(False,
                                       description="Test credentials against their service before saving.")

    def to_api_params(self) -> dict:
        return self.model_dump(exclude_none=True)


class LinkAgentParams(BaseModel):
    """Parameters for linking a workflow to an agent."""
    trigger_condition_description: Optional[str] = Field(
        None, description="Natural-language trigger condition (LLM-evaluated at runtime).")
    priority: int = Field(0, description="Execution order when multiple workflows match.")
    execution_mode_override: Optional[str] = Field(
        None, description="Override the workflow's default execution mode (sync/async).")

    def to_api_params(self) -> dict:
        return self.model_dump(exclude_none=True)


class UpdateAgentLinkParams(BaseModel):
    """Parameters for updating an agent-workflow link."""
    trigger_condition_description: Optional[str] = None
    priority: Optional[int] = None
    is_enabled: Optional[bool] = None
    execution_mode_override: Optional[str] = None

    def to_api_params(self) -> dict:
        return self.model_dump(exclude_none=True)


class ManualExecuteParams(BaseModel):
    """Parameters for manually executing a workflow."""
    context_data: Dict[str, Any] = Field(default_factory=dict,
                                         description="Data payload sent to the workflow.")
    execution_mode: Optional[str] = Field(None, description="sync or async (default: async).")

    def to_api_params(self) -> dict:
        return self.model_dump(exclude_none=True)


# Backward-compatible aliases
Workflow = WorkflowResponse
WorkflowGenerateRequest = WorkflowGenerateParams
WorkflowExecution = WorkflowExecutionResponse
WorkflowUpdate = WorkflowUpdateParams
