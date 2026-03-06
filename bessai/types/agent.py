"""Agent types for the BESS AI SDK."""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# =============================================================================
# Response Models
# =============================================================================


class AgentVersion(BaseModel):
    """A snapshot of agent configuration at a specific version."""
    version: int
    agent_type: Optional[str] = None
    agent_mode: Optional[str] = None

    # LLM / Response Engine
    system_prompt: Optional[str] = None
    greeting_message: Optional[str] = None
    llm_provider: Optional[str] = None
    llm_model: Optional[str] = None
    llm_base_url: Optional[str] = None
    temperature: Optional[float] = None
    max_completion_tokens: Optional[int] = None

    # Voice / TTS
    voice_provider: Optional[str] = None
    voice_id: Optional[str] = None
    voice_speed: Optional[float] = None
    voice_stability: Optional[float] = None
    tts_model: Optional[str] = None
    volume: Optional[float] = None
    emotion: Optional[str] = None
    tts_base_url: Optional[str] = None
    tts_sample_rate: Optional[int] = None
    tts_use_websocket: Optional[bool] = None

    # STT / Speech Recognition
    stt_provider: Optional[str] = None
    stt_model: Optional[str] = None
    stt_base_url: Optional[str] = None
    stt_multilingual: Optional[bool] = None

    # Realtime (speech-to-speech)
    realtime_provider: Optional[str] = None
    realtime_model: Optional[str] = None
    realtime_voice: Optional[str] = None

    # Behavior
    language: Optional[str] = None
    responsiveness: Optional[float] = None
    endpointing_ms: Optional[int] = None
    interruption_sensitivity: Optional[float] = None
    enable_backchannel: Optional[bool] = None
    response_delay_ms: Optional[int] = None
    end_call_after_silence_ms: Optional[int] = None
    max_call_duration_ms: Optional[int] = None
    reminder_trigger_ms: Optional[int] = None
    reminder_max_count: Optional[int] = None
    background_sound: Optional[str] = None

    # Post-call Analytics
    analytics_prompt: Optional[str] = None
    analytics_model_provider: Optional[str] = None
    analytics_model: Optional[str] = None
    enable_sentiment_analysis: Optional[bool] = None
    enable_summary_generation: Optional[bool] = None

    # Integrations
    knowledge_base_ids: Optional[List[str]] = None
    mcp_config: Optional[Dict[str, Any]] = None
    native_tools_config: Optional[Dict[str, Any]] = None

    created_at: Optional[str] = None


class LinkedWorkflow(BaseModel):
    """A workflow linked to an agent."""
    workflow_id: str
    workflow_name: Optional[str] = None
    trigger_condition_description: Optional[str] = None
    priority: int = 0
    is_enabled: bool = True
    execution_mode_override: Optional[str] = None


class AgentResponse(BaseModel):
    """Voice AI agent returned by the API."""
    agent_id: str = Field(alias="id")
    agent_name: str = Field(alias="name")
    description: Optional[str] = None
    is_published: bool = False
    published_version: Optional[int] = None
    agent_type: Optional[str] = None
    agent_mode: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    versions: Optional[List[AgentVersion]] = None
    linked_workflows: Optional[List[LinkedWorkflow]] = None

    class Config:
        populate_by_name = True


# =============================================================================
# Request Models
# =============================================================================


class AgentCreateParams(BaseModel):
    """
    Parameters for creating a voice AI agent.

    Matches the full set of configuration fields available in the BESS AI
    dashboard.  Every field except ``agent_name`` is optional and will fall
    back to sensible defaults on the server side.
    """

    # Identity
    agent_name: str = Field(..., min_length=1, max_length=255,
                            description="Display name for the agent.")
    description: Optional[str] = Field(None,
                                       description="Internal description for your reference.")
    agent_type: str = Field("orchestration_agent",
                            description="'orchestration_agent' (STT→LLM→TTS) or 'realtime_agent' (speech-to-speech).")
    agent_mode: Optional[str] = Field("single_prompt",
                                      description="'single_prompt' or 'conversation_flow'.")
    version_description: Optional[str] = Field(None,
                                               description="Description for this version snapshot.")

    # ── LLM / Response Engine ────────────────────────────────────────────
    llm_provider: str = Field("openai",
                              description="LLM provider: openai, anthropic, groq, local_llm, ollama.")
    llm_model: str = Field("gpt-4o",
                           description="Model name, e.g. gpt-4o, claude-3-5-sonnet, llama-3.3-70b-versatile.")
    llm_base_url: Optional[str] = Field(None,
                                        description="Custom base URL for self-hosted LLM (vLLM, Ollama).")
    llm_api_key: Optional[str] = Field(None,
                                       description="API key for the LLM provider (omit to use platform key).")
    system_prompt: str = Field("You are a helpful AI assistant.",
                               description="Main system instructions for the agent.")
    greeting_message: Optional[str] = Field(None,
                                            description="First utterance when agent joins the call. Empty = agent waits for user.")
    temperature: float = Field(0.7, ge=0, le=2,
                               description="LLM sampling temperature (0 = deterministic, 2 = creative).")
    max_completion_tokens: int = Field(1024, ge=1, le=8192,
                                       description="Maximum output tokens per LLM turn.")

    # ── Voice / TTS ──────────────────────────────────────────────────────
    voice_provider: str = Field("elevenlabs",
                                description="TTS provider: elevenlabs, openai, deepgram, cartesia, kokoro.")
    voice_id: str = Field("21m00Tcm4TlvDq8ikWAM",
                          description="Voice identifier from the provider's voice library.")
    voice_speed: float = Field(1.0, ge=0.5, le=2.0,
                               description="Speech rate multiplier.")
    voice_stability: float = Field(0.5, ge=0, le=1,
                                   description="Voice consistency (ElevenLabs). Lower = more expressive.")
    tts_model: Optional[str] = Field(None,
                                     description="TTS model override (eleven_turbo_v2, sonic-3, etc.).")
    volume: float = Field(1.0, ge=0, le=2,
                          description="Output volume multiplier.")
    emotion: str = Field("neutral",
                         description="Voice emotion (Cartesia sonic-3): neutral, happy, sad, angry, etc.")
    tts_base_url: Optional[str] = Field(None,
                                        description="Custom base URL for self-hosted TTS (Piper, Coqui).")
    tts_sample_rate: Optional[int] = Field(None, ge=8000, le=48000,
                                           description="Audio sample rate for local TTS.")
    tts_use_websocket: Optional[bool] = Field(None,
                                              description="Use WebSocket streaming for TTS (True) or HTTP (False).")

    # ── STT / Speech Recognition ─────────────────────────────────────────
    stt_provider: str = Field("deepgram",
                              description="STT provider: deepgram, google, azure.")
    stt_model: str = Field("nova-2",
                           description="STT model, e.g. nova-3, nova-2.")
    stt_base_url: Optional[str] = Field(None,
                                        description="Custom base URL for self-hosted STT (faster-whisper).")
    stt_api_key: Optional[str] = Field(None,
                                       description="API key for the STT provider.")
    stt_multilingual: bool = Field(False,
                                   description="Enable automatic spoken-language detection.")

    # ── Realtime (speech-to-speech) ──────────────────────────────────────
    realtime_provider: Optional[str] = Field(None,
                                             description="Realtime provider: openai, grok, google.")
    realtime_model: Optional[str] = Field(None,
                                          description="Realtime model, e.g. gpt-4o-realtime-preview.")
    realtime_voice: Optional[str] = Field(None,
                                          description="Voice for realtime model.")

    # ── Behavior ─────────────────────────────────────────────────────────
    language: str = Field("en-US",
                          description="BCP-47 language tag (en-US, tr-TR, de-DE, multi, etc.).")
    responsiveness: float = Field(1.0, ge=0, le=1,
                                  description="How quickly agent responds. 0 = slow, 1 = fast.")
    endpointing_ms: int = Field(25, ge=10, le=500,
                                description="Silence threshold (ms) before STT finalizes a user turn.")
    interruption_sensitivity: float = Field(0.8, ge=0, le=1,
                                            description="How easily user can interrupt. 0 = never, 1 = very easy.")
    enable_backchannel: bool = Field(False,
                                     description="Agent interjects 'mm-hmm', 'yeah' during long user speech.")
    response_delay_ms: int = Field(0, ge=0, le=5000,
                                   description="Artificial delay (ms) before agent responds.")
    end_call_after_silence_ms: int = Field(60000, ge=5000,
                                           description="Auto-end call after this much silence (ms). Default 60 s.")
    max_call_duration_ms: int = Field(600000, ge=60000,
                                      description="Hard cap on call length (ms). Default 10 min.")
    reminder_trigger_ms: int = Field(10000, ge=1000, le=60000,
                                     description="Remind user after this silence duration (ms).")
    reminder_max_count: int = Field(1, ge=0, le=5,
                                    description="Max reminder attempts before giving up.")
    background_sound: Optional[str] = Field(None,
                                            description="Ambient audio: coffee-shop, call-center, etc.")

    # ── Post-Call Analytics ───────────────────────────────────────────────
    analytics_prompt: Optional[str] = Field(None,
                                            description="Custom prompt for post-call analysis.")
    analytics_model_provider: Optional[str] = Field(None,
                                                    description="Provider for analytics LLM (groq, openai, anthropic).")
    analytics_model: Optional[str] = Field(None,
                                           description="Model for analytics (llama-3.3-70b-versatile, gpt-4o, etc.).")
    enable_sentiment_analysis: Optional[bool] = Field(None,
                                                      description="Enable sentiment scoring. None = org default.")
    enable_summary_generation: Optional[bool] = Field(None,
                                                      description="Enable call summary. None = org default.")

    # ── Integrations ─────────────────────────────────────────────────────
    knowledge_base_ids: Optional[List[str]] = Field(None,
                                                    description="Knowledge base IDs for RAG retrieval.")
    webhook_url: Optional[str] = Field(None,
                                       description="Webhook URL for call events (call_started, call_ended, etc.).")
    mcp_config: Optional[Dict[str, Any]] = Field(None,
                                                  description="MCP server configuration for external tools.")
    native_tools_config: Optional[Dict[str, Any]] = Field(None,
                                                           description="Built-in tools: end_call, transfer_to_human, agent_transfer, etc.")
    post_call_analysis_config: Optional[Dict[str, Any]] = Field(None,
                                                                 description="Custom post-call extraction variables.")

    def to_api_params(self) -> dict:
        """Convert to backend API parameters (name → agent_name mapping)."""
        data = self.model_dump(exclude_none=True)
        # Map SDK field names to backend field names
        if "agent_name" in data:
            data["name"] = data.pop("agent_name")
        return data


class AgentUpdateParams(BaseModel):
    """
    Parameters for updating an agent.  All fields are optional — only
    supplied fields are changed.
    """

    # Identity
    agent_name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    agent_type: Optional[str] = None
    agent_mode: Optional[str] = None
    version_description: Optional[str] = None

    # LLM
    llm_provider: Optional[str] = None
    llm_model: Optional[str] = None
    llm_base_url: Optional[str] = None
    llm_api_key: Optional[str] = None
    system_prompt: Optional[str] = None
    greeting_message: Optional[str] = None
    temperature: Optional[float] = None
    max_completion_tokens: Optional[int] = None

    # Voice / TTS
    voice_provider: Optional[str] = None
    voice_id: Optional[str] = None
    voice_speed: Optional[float] = None
    voice_stability: Optional[float] = None
    tts_model: Optional[str] = None
    volume: Optional[float] = None
    emotion: Optional[str] = None
    tts_base_url: Optional[str] = None
    tts_sample_rate: Optional[int] = None
    tts_use_websocket: Optional[bool] = None

    # STT
    stt_provider: Optional[str] = None
    stt_model: Optional[str] = None
    stt_base_url: Optional[str] = None
    stt_api_key: Optional[str] = None
    stt_multilingual: Optional[bool] = None

    # Realtime
    realtime_provider: Optional[str] = None
    realtime_model: Optional[str] = None
    realtime_voice: Optional[str] = None

    # Behavior
    language: Optional[str] = None
    responsiveness: Optional[float] = None
    endpointing_ms: Optional[int] = None
    interruption_sensitivity: Optional[float] = None
    enable_backchannel: Optional[bool] = None
    response_delay_ms: Optional[int] = None
    end_call_after_silence_ms: Optional[int] = None
    max_call_duration_ms: Optional[int] = None
    reminder_trigger_ms: Optional[int] = None
    reminder_max_count: Optional[int] = None
    background_sound: Optional[str] = None

    # Post-call Analytics
    analytics_prompt: Optional[str] = None
    analytics_model_provider: Optional[str] = None
    analytics_model: Optional[str] = None
    enable_sentiment_analysis: Optional[bool] = None
    enable_summary_generation: Optional[bool] = None

    # Integrations
    knowledge_base_ids: Optional[List[str]] = None
    webhook_url: Optional[str] = None
    mcp_config: Optional[Dict[str, Any]] = None
    native_tools_config: Optional[Dict[str, Any]] = None
    post_call_analysis_config: Optional[Dict[str, Any]] = None

    def to_api_params(self) -> dict:
        """Convert to backend API parameters."""
        data = self.model_dump(exclude_none=True)
        if "agent_name" in data:
            data["name"] = data.pop("agent_name")
        return data


# Convenience aliases matching Retell SDK naming
Agent = AgentResponse
AgentCreate = AgentCreateParams
AgentUpdate = AgentUpdateParams
