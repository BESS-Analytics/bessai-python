"""Workflows resource — generate, deploy, execute."""
from typing import Any, Dict, List, Optional

from bessai._client import SyncHTTPClient, AsyncHTTPClient
from bessai.types.workflow import Workflow, WorkflowGenerateRequest, WorkflowExecution, WorkflowUpdate


class WorkflowsResource:
    """Sync workflows resource."""

    def __init__(self, client: SyncHTTPClient):
        self._client = client

    def generate(self, **kwargs) -> Dict[str, Any]:
        """AI-generate a workflow from a description."""
        body = WorkflowGenerateRequest(**kwargs).model_dump(exclude_none=True)
        return self._client.post("/v1/workflows/generate", json=body)

    def list(
        self,
        trigger_type: Optional[str] = None,
        status: Optional[str] = None,
        agent_id: Optional[str] = None,
        page: int = 1,
        per_page: int = 20,
    ) -> List[Workflow]:
        """List workflows."""
        params = {
            "trigger_type": trigger_type, "status": status,
            "agent_id": agent_id, "page": page, "per_page": per_page,
        }
        data = self._client.get("/v1/workflows", params=params)
        items = data if isinstance(data, list) else data.get("items", data.get("workflows", []))
        return [Workflow(**w) for w in items]

    def get(self, workflow_id: str) -> Workflow:
        """Get workflow details."""
        data = self._client.get(f"/v1/workflows/{workflow_id}")
        return Workflow(**data)

    def update(self, workflow_id: str, **kwargs) -> Workflow:
        """Update a workflow."""
        body = WorkflowUpdate(**kwargs).model_dump(exclude_none=True)
        data = self._client.patch(f"/v1/workflows/{workflow_id}", json=body)
        return Workflow(**data)

    def delete(self, workflow_id: str, hard: bool = False) -> Dict[str, Any]:
        """Delete a workflow (soft-delete by default)."""
        return self._client.delete(f"/v1/workflows/{workflow_id}", params={"hard": hard} if hard else None)

    def deploy(self, workflow_id: str) -> Dict[str, Any]:
        """Deploy a workflow to n8n."""
        return self._client.post(f"/v1/workflows/{workflow_id}/deploy")

    def execute(self, workflow_id: str, context_data: Optional[Dict[str, Any]] = None) -> WorkflowExecution:
        """Manually execute a workflow."""
        body = {"context_data": context_data or {}}
        data = self._client.post(f"/v1/workflows/{workflow_id}/execute", json=body)
        return WorkflowExecution(**data)

    def test(self, workflow_id: str, test_data: Optional[Dict[str, Any]] = None) -> WorkflowExecution:
        """Test-execute a workflow."""
        body = {"test_data": test_data} if test_data else {}
        data = self._client.post(f"/v1/workflows/{workflow_id}/test", json=body)
        return WorkflowExecution(**data)

    def get_executions(self, workflow_id: str, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Get execution history for a workflow."""
        return self._client.get(
            f"/v1/workflows/{workflow_id}/executions",
            params={"page": page, "per_page": per_page},
        )


class AsyncWorkflowsResource:
    """Async workflows resource."""

    def __init__(self, client: AsyncHTTPClient):
        self._client = client

    async def generate(self, **kwargs) -> Dict[str, Any]:
        body = WorkflowGenerateRequest(**kwargs).model_dump(exclude_none=True)
        return await self._client.post("/v1/workflows/generate", json=body)

    async def list(
        self,
        trigger_type: Optional[str] = None,
        status: Optional[str] = None,
        agent_id: Optional[str] = None,
        page: int = 1,
        per_page: int = 20,
    ) -> List[Workflow]:
        params = {
            "trigger_type": trigger_type, "status": status,
            "agent_id": agent_id, "page": page, "per_page": per_page,
        }
        data = await self._client.get("/v1/workflows", params=params)
        items = data if isinstance(data, list) else data.get("items", data.get("workflows", []))
        return [Workflow(**w) for w in items]

    async def get(self, workflow_id: str) -> Workflow:
        data = await self._client.get(f"/v1/workflows/{workflow_id}")
        return Workflow(**data)

    async def update(self, workflow_id: str, **kwargs) -> Workflow:
        body = WorkflowUpdate(**kwargs).model_dump(exclude_none=True)
        data = await self._client.patch(f"/v1/workflows/{workflow_id}", json=body)
        return Workflow(**data)

    async def delete(self, workflow_id: str, hard: bool = False) -> Dict[str, Any]:
        return await self._client.delete(f"/v1/workflows/{workflow_id}", params={"hard": hard} if hard else None)

    async def deploy(self, workflow_id: str) -> Dict[str, Any]:
        return await self._client.post(f"/v1/workflows/{workflow_id}/deploy")

    async def execute(self, workflow_id: str, context_data: Optional[Dict[str, Any]] = None) -> WorkflowExecution:
        body = {"context_data": context_data or {}}
        data = await self._client.post(f"/v1/workflows/{workflow_id}/execute", json=body)
        return WorkflowExecution(**data)

    async def test(self, workflow_id: str, test_data: Optional[Dict[str, Any]] = None) -> WorkflowExecution:
        body = {"test_data": test_data} if test_data else {}
        data = await self._client.post(f"/v1/workflows/{workflow_id}/test", json=body)
        return WorkflowExecution(**data)

    async def get_executions(self, workflow_id: str, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        return await self._client.get(
            f"/v1/workflows/{workflow_id}/executions",
            params={"page": page, "per_page": per_page},
        )
