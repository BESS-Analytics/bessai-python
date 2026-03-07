"""Configuration types for the BESS AI SDK."""
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class ProviderConfig(BaseModel):
    """Full provider configuration (all categories)."""
    stt: Dict[str, Any] = {}
    llm: Dict[str, Any] = {}
    tts: Dict[str, Any] = {}
    realtime: Dict[str, Any] = {}
    analytics: Dict[str, Any] = {}
    languages: List[Any] = []
    defaults: Dict[str, Any] = {}


class DefaultsConfig(BaseModel):
    """Default configuration values."""
    stt_provider: Optional[str] = None
    stt_model: Optional[str] = None
    llm_provider: Optional[str] = None
    llm_model: Optional[str] = None
    voice_provider: Optional[str] = None
    voice_id: Optional[str] = None

    class Config:
        extra = "allow"


class LanguageEntry(BaseModel):
    """A supported language."""
    code: str
    name: str
    native_name: Optional[str] = None

    class Config:
        extra = "allow"


class ProviderPricing(BaseModel):
    """Pricing for a specific provider/model combination."""
    input_per_1k: Optional[float] = None
    output_per_1k: Optional[float] = None

    class Config:
        extra = "allow"
