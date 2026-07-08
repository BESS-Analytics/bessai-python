"""
Chat resource — text chat sessions over the same agent brain as voice
(``docs/CHAT_AGENTS_SPEC.md``).

    client.chat.create(agent_id=..., transport="rest"|"livekit")
    client.chat.send_message(session_id, content)
    client.chat.create_test_session(agent_id=..., temp_config=...)
    client.chat.retrieve(session_id)
    client.chat.list(agent_id=..., status=...)
    client.chat.close(session_id)
"""
from typing import Any, Dict, List, Optional

from bessai._client import SyncHTTPClient, AsyncHTTPClient
from bessai.types.chat import (
    ChatSession,
    ChatSessionDetail,
    ChatTurnResult,
    ChatSessionCloseResult,
    ChatSessionCreateParams,
    ChatMessageCreateParams,
    ChatTestSessionCreateParams,
)


class ChatResource:
    """Synchronous chat session operations."""

    def __init__(self, client: SyncHTTPClient):
        self._client = client

    def create(self, **kwargs) -> ChatSession:
        """Create a chat session for a published agent.

        ``transport="rest"`` (default) sessions reply via ``send_message()`` — the
        returned session's ``greeting`` carries the agent's opening line.
        ``transport="livekit"`` sessions return ``access_token``/``room_url``/
        ``room_name`` for a text-only LiveKit room instead (messages ride the
        room's ``lk.chat`` text-stream topic; the greeting arrives over the room).

        Args:
            agent_id: UUID of the published agent.
            transport: "rest" (default) or "livekit".
            channel_type: "api" (default), "web_widget", or "dashboard_test".
            dynamic_variables: Key-value pairs injected into the system prompt.
            external_user_key: Your end-user's stable id (threads sessions together).
        """
        params = ChatSessionCreateParams(**kwargs)
        data = self._client.post("/v1/chat/sessions", json=params.to_api_params())
        return ChatSession(**data)

    def create_test_session(self, **kwargs) -> ChatSession:
        """Create a dashboard-style test chat session (mirror of ``call.create_test_call``).

        Accepts **draft (unpublished)** agents and a ``temp_config`` override that is
        not persisted. REST transport only — fastest loop for iterating on a prompt.

        Args:
            agent_id: UUID of the agent (published or draft).
            temp_config: Dict of config overrides (system_prompt, etc.), not saved.
            dynamic_variables: Key-value pairs injected into the system prompt.
        """
        params = ChatTestSessionCreateParams(**kwargs)
        data = self._client.post("/v1/chat/test", json=params.to_api_params())
        return ChatSession(**data)

    def send_message(self, session_id: str, content: str) -> ChatTurnResult:
        """Send a user message on a REST-transport session and get the reply (sync JSON).

        Raises on ``livekit``-transport sessions (409) — send those over the room's
        ``lk.chat`` text stream instead.

        Args:
            session_id: UUID of the chat session.
            content: User message, 1-4,000 characters.
        """
        params = ChatMessageCreateParams(content=content)
        data = self._client.post(
            f"/v1/chat/sessions/{session_id}/messages", json=params.to_api_params()
        )
        return ChatTurnResult(**data)

    def retrieve(self, session_id: str, skip: int = 0, limit: int = 50) -> ChatSessionDetail:
        """Get session detail plus its paginated message thread (oldest first).

        Args:
            session_id: UUID of the chat session.
            skip: Message pagination offset (default 0).
            limit: Messages per page, 1-200 (default 50).
        """
        data = self._client.get(
            f"/v1/chat/sessions/{session_id}", params={"skip": skip, "limit": limit}
        )
        return ChatSessionDetail(**data)

    def list(
        self,
        skip: int = 0,
        limit: int = 20,
        agent_id: Optional[str] = None,
        status: Optional[str] = None,
        channel_type: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> List[ChatSession]:
        """List chat sessions with optional filters (newest first).

        Args:
            skip: Pagination offset (default 0).
            limit: Page size, 1-200 (default 20).
            agent_id: Filter by agent UUID.
            status: Filter by status (active, idle, closed).
            channel_type: Filter by channel (api, web_widget, dashboard_test).
            from_date: ISO 8601 start date filter.
            to_date: ISO 8601 end date filter.
        """
        params: Dict[str, Any] = {"skip": skip, "limit": limit}
        if agent_id is not None:
            params["agent_id"] = agent_id
        if status is not None:
            params["status"] = status
        if channel_type is not None:
            params["channel_type"] = channel_type
        if from_date is not None:
            params["from_date"] = from_date
        if to_date is not None:
            params["to_date"] = to_date

        data = self._client.get("/v1/chat/sessions", params=params)
        items = data if isinstance(data, list) else data.get("items", [])
        return [ChatSession(**s) for s in items]

    def close(self, session_id: str) -> ChatSessionCloseResult:
        """Explicitly close a chat session (queues summary/sentiment/automation).

        Args:
            session_id: UUID of the chat session.
        """
        data = self._client.post(f"/v1/chat/sessions/{session_id}/close")
        return ChatSessionCloseResult(**data)


class AsyncChatResource:
    """Asynchronous chat session operations."""

    def __init__(self, client: AsyncHTTPClient):
        self._client = client

    async def create(self, **kwargs) -> ChatSession:
        """Create a chat session for a published agent."""
        params = ChatSessionCreateParams(**kwargs)
        data = await self._client.post("/v1/chat/sessions", json=params.to_api_params())
        return ChatSession(**data)

    async def create_test_session(self, **kwargs) -> ChatSession:
        """Create a dashboard-style test chat session."""
        params = ChatTestSessionCreateParams(**kwargs)
        data = await self._client.post("/v1/chat/test", json=params.to_api_params())
        return ChatSession(**data)

    async def send_message(self, session_id: str, content: str) -> ChatTurnResult:
        """Send a user message on a REST-transport session and get the reply."""
        params = ChatMessageCreateParams(content=content)
        data = await self._client.post(
            f"/v1/chat/sessions/{session_id}/messages", json=params.to_api_params()
        )
        return ChatTurnResult(**data)

    async def retrieve(self, session_id: str, skip: int = 0, limit: int = 50) -> ChatSessionDetail:
        """Get session detail plus its paginated message thread."""
        data = await self._client.get(
            f"/v1/chat/sessions/{session_id}", params={"skip": skip, "limit": limit}
        )
        return ChatSessionDetail(**data)

    async def list(
        self,
        skip: int = 0,
        limit: int = 20,
        agent_id: Optional[str] = None,
        status: Optional[str] = None,
        channel_type: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> List[ChatSession]:
        """List chat sessions with optional filters."""
        params: Dict[str, Any] = {"skip": skip, "limit": limit}
        if agent_id is not None:
            params["agent_id"] = agent_id
        if status is not None:
            params["status"] = status
        if channel_type is not None:
            params["channel_type"] = channel_type
        if from_date is not None:
            params["from_date"] = from_date
        if to_date is not None:
            params["to_date"] = to_date

        data = await self._client.get("/v1/chat/sessions", params=params)
        items = data if isinstance(data, list) else data.get("items", [])
        return [ChatSession(**s) for s in items]

    async def close(self, session_id: str) -> ChatSessionCloseResult:
        """Explicitly close a chat session."""
        data = await self._client.post(f"/v1/chat/sessions/{session_id}/close")
        return ChatSessionCloseResult(**data)


# Backward-compatible aliases
ChatsResource = ChatResource
AsyncChatsResource = AsyncChatResource
