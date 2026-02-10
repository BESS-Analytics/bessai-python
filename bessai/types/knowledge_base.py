"""Knowledge base types for the BESS AI SDK."""
from typing import List, Optional
from pydantic import BaseModel


class Document(BaseModel):
    """Document in a knowledge base."""
    id: str
    filename: Optional[str] = None
    file_type: Optional[str] = None
    file_size_bytes: Optional[int] = None
    status: Optional[str] = None
    chunk_count: Optional[int] = None
    created_at: Optional[str] = None


class KnowledgeBase(BaseModel):
    """Knowledge base for RAG."""
    id: str
    name: str
    description: Optional[str] = None
    documents: Optional[List[Document]] = None
    created_at: Optional[str] = None


class KnowledgeBaseCreate(BaseModel):
    """Parameters for creating a knowledge base."""
    name: str
    description: Optional[str] = None
