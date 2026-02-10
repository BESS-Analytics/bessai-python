"""
BESS AI Python SDK
==================

Official Python SDK for the BESS AI Voice Platform.

Quickstart (sync):

    from bessai import BessAI

    client = BessAI(api_key="bess_sk_live_...")

    agent = client.agents.create(
        name="Support Agent",
        llm_provider="openai",
        llm_model="gpt-4o",
        system_prompt="You are a helpful support agent.",
    )

    call = client.calls.create_phone_call(
        agent_id=agent.id,
        from_number="+14157774444",
        to_number="+12137774445",
    )

Quickstart (async):

    from bessai import AsyncBessAI

    async def main():
        client = AsyncBessAI(api_key="bess_sk_live_...")
        agents = await client.agents.list()
        await client.close()
"""
from typing import Dict, Optional

from bessai._version import __version__
from bessai._config import ClientConfig, DEFAULT_BASE_URL, DEFAULT_TIMEOUT, DEFAULT_MAX_RETRIES
from bessai._client import SyncHTTPClient, AsyncHTTPClient
from bessai._streaming import StreamingResource

# Resource classes
from bessai.resources.agents import AgentsResource, AsyncAgentsResource
from bessai.resources.calls import CallsResource, AsyncCallsResource
from bessai.resources.phone_numbers import PhoneNumbersResource, AsyncPhoneNumbersResource
from bessai.resources.batch_calls import BatchCallsResource, AsyncBatchCallsResource
from bessai.resources.workflows import WorkflowsResource, AsyncWorkflowsResource
from bessai.resources.analytics import AnalyticsResource, AsyncAnalyticsResource
from bessai.resources.knowledge_bases import KnowledgeBasesResource, AsyncKnowledgeBasesResource
from bessai.resources.api_keys import APIKeysResource, AsyncAPIKeysResource

# Exceptions (re-export for convenience)
from bessai._exceptions import (
    BessAIError,
    AuthenticationError,
    PermissionDeniedError,
    NotFoundError,
    ValidationError,
    RateLimitError,
    InternalServerError,
    ConnectionError,
    TimeoutError,
)


class BessAI:
    """
    Synchronous BESS AI client.

    Args:
        api_key: Your BESS AI API key (or set BESSAI_API_KEY env var).
        base_url: API base URL (default: https://api.bessai.com).
        timeout: Request timeout in seconds (default: 30).
        max_retries: Max retry attempts for transient errors (default: 3).
        headers: Additional headers to include in all requests.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        headers: Optional[Dict[str, str]] = None,
    ):
        self._config = ClientConfig.from_env(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            headers=headers or {},
        )
        self._http = SyncHTTPClient(self._config)

        # Resource namespaces
        self.agents = AgentsResource(self._http)
        self.calls = CallsResource(self._http)
        self.phone_numbers = PhoneNumbersResource(self._http)
        self.batch_calls = BatchCallsResource(self._http)
        self.workflows = WorkflowsResource(self._http)
        self.analytics = AnalyticsResource(self._http)
        self.knowledge_bases = KnowledgeBasesResource(self._http)
        self.api_keys = APIKeysResource(self._http)

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._http.close()

    def __enter__(self) -> "BessAI":
        return self

    def __exit__(self, *args) -> None:
        self.close()

    def __repr__(self) -> str:
        return f"BessAI(base_url={self._config.base_url!r})"


class AsyncBessAI:
    """
    Asynchronous BESS AI client.

    Args:
        api_key: Your BESS AI API key (or set BESSAI_API_KEY env var).
        base_url: API base URL (default: https://api.bessai.com).
        timeout: Request timeout in seconds (default: 30).
        max_retries: Max retry attempts for transient errors (default: 3).
        headers: Additional headers to include in all requests.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        headers: Optional[Dict[str, str]] = None,
    ):
        self._config = ClientConfig.from_env(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            headers=headers or {},
        )
        self._http = AsyncHTTPClient(self._config)

        # Resource namespaces
        self.agents = AsyncAgentsResource(self._http)
        self.calls = AsyncCallsResource(self._http)
        self.phone_numbers = AsyncPhoneNumbersResource(self._http)
        self.batch_calls = AsyncBatchCallsResource(self._http)
        self.workflows = AsyncWorkflowsResource(self._http)
        self.analytics = AsyncAnalyticsResource(self._http)
        self.knowledge_bases = AsyncKnowledgeBasesResource(self._http)
        self.api_keys = AsyncAPIKeysResource(self._http)
        self.streaming = StreamingResource(self._config)

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        await self._http.close()

    async def __aenter__(self) -> "AsyncBessAI":
        return self

    async def __aexit__(self, *args) -> None:
        await self.close()

    def __repr__(self) -> str:
        return f"AsyncBessAI(base_url={self._config.base_url!r})"


__all__ = [
    # Client classes
    "BessAI",
    "AsyncBessAI",
    # Version
    "__version__",
    # Exceptions
    "BessAIError",
    "AuthenticationError",
    "PermissionDeniedError",
    "NotFoundError",
    "ValidationError",
    "RateLimitError",
    "InternalServerError",
    "ConnectionError",
    "TimeoutError",
]
