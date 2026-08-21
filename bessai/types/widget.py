"""Widget types for the BESS AI SDK — the embeddable voice/chat widget."""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class Widget(BaseModel):
    """An embeddable widget. ``public_key`` (``bess_pk_live_…``) is publishable —
    safe to ship in client-side code. ``embed_code`` is the ready-to-paste
    ``<script>`` install snippet built server-side from the widget's branding."""
    id: str
    organization_id: Optional[str] = None
    agent_id: Optional[str] = None
    # Advanced, usually ``None``: a second published agent serving the VOICE
    # surface only, so a hybrid widget can run speech-to-speech voice while chat
    # keeps a cascade agent. ``None`` means ``agent_id`` serves both.
    voice_agent_id: Optional[str] = None
    public_key: str
    name: Optional[str] = None
    allowed_origins: Optional[List[str]] = None
    locale: Optional[str] = None
    branding: Optional[Dict[str, Any]] = None
    mode: Optional[str] = None  # voice | chat | hybrid
    max_call_seconds: Optional[int] = None
    max_messages_per_session: Optional[int] = None
    rate_per_minute: Optional[int] = None
    rate_per_day: Optional[int] = None
    daily_session_cap: Optional[int] = None
    require_captcha: Optional[bool] = None
    is_active: Optional[bool] = None
    embed_code: Optional[str] = None  # ready-to-paste <script> tag
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class WidgetCreateParams(BaseModel):
    """Parameters for creating a widget (agent must be PUBLISHED)."""
    agent_id: str
    # Optional second PUBLISHED agent for the VOICE surface only; chat always uses
    # ``agent_id``. Omit it — the default — and one agent serves both surfaces.
    # Note: ``update()`` strips ``None`` values, so clearing an existing split
    # needs a direct PATCH with ``{"voice_agent_id": null}``.
    voice_agent_id: Optional[str] = None
    name: str
    allowed_origins: Optional[List[str]] = None
    locale: Optional[str] = None  # 'tr' | 'en'
    branding: Optional[Dict[str, Any]] = None
    mode: Optional[str] = None  # voice | chat | hybrid
    max_call_seconds: Optional[int] = None
    max_messages_per_session: Optional[int] = None
    rate_per_minute: Optional[int] = None
    rate_per_day: Optional[int] = None
    daily_session_cap: Optional[int] = None
    require_captcha: Optional[bool] = None


class WidgetEntitlement(BaseModel):
    """Unlock state of the widget product family ('widget' = voice, 'chat_widget' = chat)."""
    unlocked: bool
    source: Optional[str] = None  # 'credit' | 'comp' | 'admin'
    unlocked_at: Optional[str] = None
    price_usd: Optional[float] = None
    features: Optional[Dict[str, Any]] = None
