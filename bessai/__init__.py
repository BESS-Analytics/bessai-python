"""
BESS AI Python SDK
==================

Official Python SDK for the BESS AI Voice Platform.

Quickstart (sync):

    from bessai import BessAI

    client = BessAI(api_key="bess_sk_live_...")

    agent = client.agent.create(
        agent_name="Support Agent",
        llm_provider="openai",
        llm_model="gpt-4o",
        system_prompt="You are a helpful support agent.",
    )

    call = client.calls.create_phone_call(
        agent_id=agent.agent_id,
        from_number="+14157774444",
        to_number="+12137774445",
    )

Quickstart (async):

    from bessai import AsyncBessAI

    async def main():
        client = AsyncBessAI(api_key="bess_sk_live_...")
        agents = await client.agent.list()
        await client.close()
"""
from typing import Dict, Optional

from bessai._version import __version__
from bessai._config import ClientConfig, DEFAULT_BASE_URL, DEFAULT_TIMEOUT, DEFAULT_MAX_RETRIES
from bessai._client import SyncHTTPClient, AsyncHTTPClient
from bessai._streaming import StreamingResource

# Resource classes
from bessai.resources.agents import AgentResource, AsyncAgentResource
from bessai.resources.calls import CallResource, AsyncCallResource
from bessai.resources.phone_numbers import PhoneNumberResource, AsyncPhoneNumberResource
from bessai.resources.batch_calls import BatchCallResource, AsyncBatchCallResource
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

        # Resource namespaces (singular = Retell-compatible convention)
        self.agent = AgentResource(self._http)
        self.call = CallResource(self._http)
        self.phone_number = PhoneNumberResource(self._http)
        self.batch_call = BatchCallResource(self._http)
        self.workflows = WorkflowsResource(self._http)
        self.analytics = AnalyticsResource(self._http)
        self.knowledge_bases = KnowledgeBasesResource(self._http)
        self.api_keys = APIKeysResource(self._http)

    @property
    def agents(self) -> AgentResource:
        """Backward-compatible alias for ``self.agent``."""
        return self.agent

    @property
    def calls(self) -> CallResource:
        """Backward-compatible alias for ``self.call``."""
        return self.call

    @property
    def phone_numbers(self) -> PhoneNumberResource:
        """Backward-compatible alias for ``self.phone_number``."""
        return self.phone_number

    @property
    def batch_calls(self) -> BatchCallResource:
        """Backward-compatible alias for ``self.batch_call``."""
        return self.batch_call

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

        # Resource namespaces (singular = Retell-compatible convention)
        self.agent = AsyncAgentResource(self._http)
        self.call = AsyncCallResource(self._http)
        self.phone_number = AsyncPhoneNumberResource(self._http)
        self.batch_call = AsyncBatchCallResource(self._http)
        self.workflows = AsyncWorkflowsResource(self._http)
        self.analytics = AsyncAnalyticsResource(self._http)
        self.knowledge_bases = AsyncKnowledgeBasesResource(self._http)
        self.api_keys = AsyncAPIKeysResource(self._http)
        self.streaming = StreamingResource(self._config)

    @property
    def agents(self) -> AsyncAgentResource:
        """Backward-compatible alias for ``self.agent``."""
        return self.agent

    @property
    def calls(self) -> AsyncCallResource:
        """Backward-compatible alias for ``self.call``."""
        return self.call

    @property
    def phone_numbers(self) -> AsyncPhoneNumberResource:
        """Backward-compatible alias for ``self.phone_number``."""
        return self.phone_number

    @property
    def batch_calls(self) -> AsyncBatchCallResource:
        """Backward-compatible alias for ``self.batch_call``."""
        return self.batch_call

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
