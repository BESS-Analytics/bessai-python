"""
BESS AI SDK Configuration.
"""
import os
from dataclasses import dataclass, field
from typing import Optional, Dict


DEFAULT_BASE_URL = "https://api.bessai.com"
DEFAULT_TIMEOUT = 30.0
DEFAULT_MAX_RETRIES = 3

# Environment variable names
ENV_API_KEY = "BESSAI_API_KEY"
ENV_BASE_URL = "BESSAI_BASE_URL"


@dataclass
class ClientConfig:
    """Configuration for the BESS AI client."""

    api_key: str
    base_url: str = DEFAULT_BASE_URL
    timeout: float = DEFAULT_TIMEOUT
    max_retries: int = DEFAULT_MAX_RETRIES
    headers: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_env(
        cls,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        **kwargs,
    ) -> "ClientConfig":
        """
        Create config from environment variables with optional overrides.

        Environment variables:
            BESSAI_API_KEY: API key (required if api_key not passed)
            BESSAI_BASE_URL: Base URL override
        """
        resolved_key = api_key or os.environ.get(ENV_API_KEY, "")
        if not resolved_key:
            raise ValueError(
                f"API key is required. Pass api_key= or set {ENV_API_KEY} environment variable."
            )

        resolved_url = base_url or os.environ.get(ENV_BASE_URL, DEFAULT_BASE_URL)

        return cls(
            api_key=resolved_key,
            base_url=resolved_url.rstrip("/"),
            **kwargs,
        )
