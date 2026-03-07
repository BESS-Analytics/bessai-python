"""Config resource — provider configuration, defaults, languages, and pricing.

All config endpoints are public (no authentication required).

Usage (sync)::

    providers = client.config.get_providers()
    stt       = client.config.get_provider("stt")
    defaults  = client.config.get_defaults()
    langs     = client.config.get_languages()

Usage (async)::

    providers = await client.config.get_providers()
"""
from typing import Any, Dict, List

from bessai._client import SyncHTTPClient, AsyncHTTPClient
from bessai.types.config import ProviderConfig


class ConfigResource:
    """Sync config resource — ``client.config``."""

    def __init__(self, client: SyncHTTPClient):
        self._client = client

    def get_providers(self) -> ProviderConfig:
        """Get the complete provider configuration (STT, LLM, TTS, etc.)."""
        data = self._client.get("/v1/config/providers")
        return ProviderConfig(**data)

    def get_provider(self, provider_type: str) -> Dict[str, Any]:
        """Get providers for a specific type.

        Args:
            provider_type: One of ``stt``, ``llm``, ``tts``, ``realtime``,
                ``analytics``.
        """
        return self._client.get(f"/v1/config/providers/{provider_type}")

    def get_defaults(self) -> Dict[str, Any]:
        """Get default configuration values."""
        return self._client.get("/v1/config/defaults")

    def get_languages(self) -> List[Any]:
        """Get list of supported languages."""
        return self._client.get("/v1/config/languages")


class AsyncConfigResource:
    """Async config resource — ``client.config``."""

    def __init__(self, client: AsyncHTTPClient):
        self._client = client

    async def get_providers(self) -> ProviderConfig:
        """Get the complete provider configuration."""
        data = await self._client.get("/v1/config/providers")
        return ProviderConfig(**data)

    async def get_provider(self, provider_type: str) -> Dict[str, Any]:
        """Get providers for a specific type."""
        return await self._client.get(f"/v1/config/providers/{provider_type}")

    async def get_defaults(self) -> Dict[str, Any]:
        """Get default configuration values."""
        return await self._client.get("/v1/config/defaults")

    async def get_languages(self) -> List[Any]:
        """Get list of supported languages."""
        return await self._client.get("/v1/config/languages")


