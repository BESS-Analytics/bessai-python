"""Agent types for the BESS AI SDK."""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class AgentVersion(BaseModel):
    """Agent configuration version."""
    version: int
    agent_type: Optional[str] = None
    system_prompt: Optional[str] = None
    greeting_message: Optional[str] = None
    llm_provider: Optional[str] = None
    llm_model: Optional[str] = None
    voice_provider: Optional[str] = None
    voice_id: Optional[str] = None
    stt_provider: Optional[str] = None
    stt_model: Optional[str] = None
    stt_multilingual: Optional[bool] = None
    realtime_provider: Optional[str] = None
    realtime_model: Optional[str] = None
    realtime_voice: Optional[str] = None
    language: Optional[str] = None
    knowledge_base_ids: Optional[List[str]] = None
    temperature: Optional[float] = None
    max_completion_tokens: Optional[int] = None
    tts_model: Optional[str] = None
    volume: Optional[float] = None
    voice_speed: Optional[float] = None
    voice_stability: Optional[float] = None
    interruption_sensitivity: Optional[float] = None
    responsiveness: Optional[float] = None
    endpointing_ms: Optional[int] = None
    reminder_trigger_ms: Optional[int] = None
    reminder_max_count: Optional[int] = None
    max_call_duration_ms: Optional[int] = None
    end_call_after_silence_ms: Optional[int] = None
    background_sound: Optional[str] = None
    analytics_prompt: Optional[str] = None
    analytics_model_provider: Optional[str] = None
    analytics_model: Optional[str] = None
    enable_sentiment_analysis: Optional[bool] = None
    enable_summary_generation: Optional[bool] = None
    mcp_config: Optional[Dict[str, Any]] = None
    native_tools_config: Optional[Dict[str, Any]] = None
    created_at: Optional[str] = None


class Agent(BaseModel):
    """Voice AI agent."""
    id: str
    name: str
    description: Optional[str] = None
    is_published: bool = False
    published_version: Optional[int] = None
    agent_type: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    versions: Optional[List[AgentVersion]] = None


class AgentCreate(BaseModel):
    """Parameters for creating an agent."""
    name: str
    description: Optional[str] = None
    agent_type: Optional[str] = "orchestration_agent"
    system_prompt: Optional[str] = None
    greeting_message: Optional[str] = None
    llm_provider: Optional[str] = "openai"
    llm_model: Optional[str] = "gpt-4o"
    voice_provider: Optional[str] = "elevenlabs"
    voice_id: Optional[str] = None
    stt_provider: Optional[str] = "deepgram"
    stt_model: Optional[str] = "nova-2"
    language: Optional[str] = "en-US"
    temperature: Optional[float] = None
    max_completion_tokens: Optional[int] = None
    knowledge_base_ids: Optional[List[str]] = None
    tools_config: Optional[List[Dict[str, Any]]] = None
    webhook_url: Optional[str] = None


class AgentUpdate(BaseModel):
    """Parameters for updating an agent."""
    name: Optional[str] = None
    description: Optional[str] = None
    system_prompt: Optional[str] = None
    greeting_message: Optional[str] = None
    llm_provider: Optional[str] = None
    llm_model: Optional[str] = None
    voice_provider: Optional[str] = None
    voice_id: Optional[str] = None
    stt_provider: Optional[str] = None
    stt_model: Optional[str] = None
    language: Optional[str] = None
    temperature: Optional[float] = None
    max_completion_tokens: Optional[int] = None
    knowledge_base_ids: Optional[List[str]] = None
