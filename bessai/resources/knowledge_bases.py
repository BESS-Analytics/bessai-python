"""Knowledge bases resource — RAG document management."""
from typing import Any, Dict, List, Optional, Tuple

from bessai._client import SyncHTTPClient, AsyncHTTPClient
from bessai.types.knowledge_base import KnowledgeBase, KnowledgeBaseCreate, Document


class KnowledgeBasesResource:
    """Sync knowledge bases resource."""

    def __init__(self, client: SyncHTTPClient):
        self._client = client

    def create(self, **kwargs) -> KnowledgeBase:
        """Create a knowledge base."""
        body = KnowledgeBaseCreate(**kwargs).model_dump(exclude_none=True)
        data = self._client.post("/v1/knowledge-bases", json=body)
        return KnowledgeBase(**data)

    def list(self, skip: int = 0, limit: int = 20) -> List[KnowledgeBase]:
        """List knowledge bases."""
        data = self._client.get("/v1/knowledge-bases", params={"skip": skip, "limit": limit})
        items = data if isinstance(data, list) else data.get("items", [])
        return [KnowledgeBase(**k) for k in items]

    def get(self, kb_id: str) -> KnowledgeBase:
        """Get knowledge base details."""
        data = self._client.get(f"/v1/knowledge-bases/{kb_id}")
        return KnowledgeBase(**data)

    def delete(self, kb_id: str) -> None:
        """Delete a knowledge base."""
        self._client.delete(f"/v1/knowledge-bases/{kb_id}")

    def upload_document(self, kb_id: str, file_path: str, filename: Optional[str] = None) -> Document:
        """Upload a document to a knowledge base."""
        import os
        fname = filename or os.path.basename(file_path)
        with open(file_path, "rb") as f:
            data = self._client.request(
                "POST",
                f"/v1/knowledge-bases/{kb_id}/documents",
                files={"file": (fname, f)},
            )
        return Document(**data)

    def delete_document(self, kb_id: str, document_id: str) -> None:
        """Delete a document from a knowledge base."""
        self._client.delete(f"/v1/knowledge-bases/{kb_id}/documents/{document_id}")


class AsyncKnowledgeBasesResource:
    """Async knowledge bases resource."""

    def __init__(self, client: AsyncHTTPClient):
        self._client = client

    async def create(self, **kwargs) -> KnowledgeBase:
        body = KnowledgeBaseCreate(**kwargs).model_dump(exclude_none=True)
        data = await self._client.post("/v1/knowledge-bases", json=body)
        return KnowledgeBase(**data)

    async def list(self, skip: int = 0, limit: int = 20) -> List[KnowledgeBase]:
        data = await self._client.get("/v1/knowledge-bases", params={"skip": skip, "limit": limit})
        items = data if isinstance(data, list) else data.get("items", [])
        return [KnowledgeBase(**k) for k in items]

    async def get(self, kb_id: str) -> KnowledgeBase:
        data = await self._client.get(f"/v1/knowledge-bases/{kb_id}")
        return KnowledgeBase(**data)

    async def delete(self, kb_id: str) -> None:
        await self._client.delete(f"/v1/knowledge-bases/{kb_id}")

    async def upload_document(self, kb_id: str, file_path: str, filename: Optional[str] = None) -> Document:
        """Upload a document to a knowledge base."""
        import os
        fname = filename or os.path.basename(file_path)
        with open(file_path, "rb") as f:
            data = await self._client.request(
                "POST",
                f"/v1/knowledge-bases/{kb_id}/documents",
                files={"file": (fname, f)},
            )
        return Document(**data)

    async def delete_document(self, kb_id: str, document_id: str) -> None:
        await self._client.delete(f"/v1/knowledge-bases/{kb_id}/documents/{document_id}")
