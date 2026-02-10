"""Workflow types for the BESS AI SDK."""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class WorkflowGenerateRequest(BaseModel):
    """Parameters for AI-generating a workflow."""
    name: str
    description: str
    trigger_type: str = "api"
    trigger_config: Optional[Dict[str, Any]] = None
    agent_id: Optional[str] = None


class Workflow(BaseModel):
    """Workflow entity."""
    id: str
    name: Optional[str] = None
    description: Optional[str] = None
    trigger_type: Optional[str] = None
    status: Optional[str] = None
    is_active: Optional[bool] = None
    workflow_json: Optional[Dict[str, Any]] = None
    n8n_workflow_id: Optional[str] = None
    agent_id: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class WorkflowExecution(BaseModel):
    """Workflow execution result."""
    execution_id: Optional[str] = None
    status: Optional[str] = None
    execution_time_ms: Optional[int] = None
    output: Optional[Any] = None
    error: Optional[str] = None


class WorkflowUpdate(BaseModel):
    """Parameters for updating a workflow."""
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    status: Optional[str] = None
    execution_mode: Optional[str] = None
    timeout_seconds: Optional[int] = None
