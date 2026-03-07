"""
BESS AI SDK — Base HTTP Client.

Provides both sync (httpx.Client) and async (httpx.AsyncClient) wrappers
with automatic auth, retries, and error mapping.
"""
import time
from typing import Any, Dict, Optional, Type, TypeVar, Union, List

import httpx

from bessai._config import ClientConfig
from bessai._exceptions import (
    BessAIError,
    ConnectionError,
    RateLimitError,
    TimeoutError,
    raise_for_status,
)
from bessai._version import __version__

T = TypeVar("T")

_USER_AGENT = f"bessai-python/{__version__}"

# Status codes that trigger automatic retry
_RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}


def _build_headers(config: ClientConfig) -> Dict[str, str]:
    """Build default headers for all requests."""
    headers = {
        "Authorization": f"Bearer {config.api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": _USER_AGENT,
    }
    headers.update(config.headers)
    return headers


def _backoff_delay(attempt: int, retry_after: Optional[float] = None) -> float:
    """Exponential backoff with jitter. Respects Retry-After header."""
    if retry_after and retry_after > 0:
        return min(retry_after, 60.0)
    return min(0.5 * (2 ** attempt), 30.0)


# =============================================================================
# Synchronous Client
# =============================================================================

class SyncHTTPClient:
    """Synchronous HTTP client wrapping httpx.Client."""

    def __init__(self, config: ClientConfig):
        self._config = config
        self._client = httpx.Client(
            base_url=config.base_url,
            headers=_build_headers(config),
            timeout=httpx.Timeout(config.timeout),
        )

    def request(
        self,
        method: str,
        path: str,
        *,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        files: Optional[Any] = None,
        content_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Make an HTTP request with automatic retries and error handling."""
        # Clean None values from params
        if params:
            params = {k: v for k, v in params.items() if v is not None}

        headers = {}
        if content_type:
            headers["Content-Type"] = content_type
        if files:
            headers.pop("Content-Type", None)

        last_error: Optional[Exception] = None
        for attempt in range(self._config.max_retries + 1):
            try:
                response = self._client.request(
                    method,
                    path,
                    json=json,
                    params=params,
                    data=data,
                    files=files,
                    headers=headers if headers else None,
                )

                if response.status_code in _RETRYABLE_STATUS_CODES and attempt < self._config.max_retries:
                    retry_after = _parse_retry_after(response)
                    time.sleep(_backoff_delay(attempt, retry_after))
                    continue

                if response.status_code == 204:
                    return {}

                body = response.json() if response.content else {}
                raise_for_status(response.status_code, body)
                return body

            except (httpx.ConnectError, httpx.ConnectTimeout) as e:
                last_error = ConnectionError(str(e))
                if attempt < self._config.max_retries:
                    time.sleep(_backoff_delay(attempt))
                    continue
            except httpx.ReadTimeout as e:
                last_error = TimeoutError(str(e))
                if attempt < self._config.max_retries:
                    time.sleep(_backoff_delay(attempt))
                    continue
            except (BessAIError, RateLimitError):
                raise
            except httpx.HTTPError as e:
                last_error = BessAIError(str(e))
                if attempt < self._config.max_retries:
                    time.sleep(_backoff_delay(attempt))
                    continue

        raise last_error or BessAIError("Request failed after retries")

    def get(self, path: str, **kwargs) -> Dict[str, Any]:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs) -> Dict[str, Any]:
        return self.request("POST", path, **kwargs)

    def patch(self, path: str, **kwargs) -> Dict[str, Any]:
        return self.request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs) -> Dict[str, Any]:
        return self.request("DELETE", path, **kwargs)

    def get_bytes(self, path: str, **kwargs) -> bytes:
        """GET request returning raw bytes (for file downloads)."""
        params = kwargs.get("params")
        if params:
            params = {k: v for k, v in params.items() if v is not None}
        response = self._client.request("GET", path, params=params)
        raise_for_status(response.status_code, response.json() if response.headers.get("content-type", "").startswith("application/json") else {})
        return response.content

    def close(self) -> None:
        self._client.close()


# =============================================================================
# Asynchronous Client
# =============================================================================

class AsyncHTTPClient:
    """Asynchronous HTTP client wrapping httpx.AsyncClient."""

    def __init__(self, config: ClientConfig):
        self._config = config
        self._client = httpx.AsyncClient(
            base_url=config.base_url,
            headers=_build_headers(config),
            timeout=httpx.Timeout(config.timeout),
        )

    async def request(
        self,
        method: str,
        path: str,
        *,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        files: Optional[Any] = None,
        content_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Make an async HTTP request with automatic retries and error handling."""
        import asyncio

        if params:
            params = {k: v for k, v in params.items() if v is not None}

        headers = {}
        if content_type:
            headers["Content-Type"] = content_type
        if files:
            headers.pop("Content-Type", None)

        last_error: Optional[Exception] = None
        for attempt in range(self._config.max_retries + 1):
            try:
                response = await self._client.request(
                    method,
                    path,
                    json=json,
                    params=params,
                    data=data,
                    files=files,
                    headers=headers if headers else None,
                )

                if response.status_code in _RETRYABLE_STATUS_CODES and attempt < self._config.max_retries:
                    retry_after = _parse_retry_after(response)
                    await asyncio.sleep(_backoff_delay(attempt, retry_after))
                    continue

                if response.status_code == 204:
                    return {}

                body = response.json() if response.content else {}
                raise_for_status(response.status_code, body)
                return body

            except (httpx.ConnectError, httpx.ConnectTimeout) as e:
                last_error = ConnectionError(str(e))
                if attempt < self._config.max_retries:
                    await asyncio.sleep(_backoff_delay(attempt))
                    continue
            except httpx.ReadTimeout as e:
                last_error = TimeoutError(str(e))
                if attempt < self._config.max_retries:
                    await asyncio.sleep(_backoff_delay(attempt))
                    continue
            except (BessAIError, RateLimitError):
                raise
            except httpx.HTTPError as e:
                last_error = BessAIError(str(e))
                if attempt < self._config.max_retries:
                    await asyncio.sleep(_backoff_delay(attempt))
                    continue

        raise last_error or BessAIError("Request failed after retries")

    async def get(self, path: str, **kwargs) -> Dict[str, Any]:
        return await self.request("GET", path, **kwargs)

    async def post(self, path: str, **kwargs) -> Dict[str, Any]:
        return await self.request("POST", path, **kwargs)

    async def patch(self, path: str, **kwargs) -> Dict[str, Any]:
        return await self.request("PATCH", path, **kwargs)

    async def delete(self, path: str, **kwargs) -> Dict[str, Any]:
        return await self.request("DELETE", path, **kwargs)

    async def get_bytes(self, path: str, **kwargs) -> bytes:
        """GET request returning raw bytes (for file downloads)."""
        params = kwargs.get("params")
        if params:
            params = {k: v for k, v in params.items() if v is not None}
        response = await self._client.request("GET", path, params=params)
        raise_for_status(response.status_code, response.json() if response.headers.get("content-type", "").startswith("application/json") else {})
        return response.content

    async def close(self) -> None:
        await self._client.aclose()


# =============================================================================
# Helpers
# =============================================================================

def _parse_retry_after(response: httpx.Response) -> Optional[float]:
    """Parse Retry-After header (seconds)."""
    val = response.headers.get("Retry-After")
    if val:
        try:
            return float(val)
        except ValueError:
            pass
    return None
