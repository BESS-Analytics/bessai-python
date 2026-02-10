"""Analytics types for the BESS AI SDK."""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class LatencyPercentiles(BaseModel):
    """Latency percentile metrics."""
    p50: Optional[float] = None
    p90: Optional[float] = None
    p95: Optional[float] = None
    p99: Optional[float] = None


class LatencyMetrics(BaseModel):
    """Latency metrics across pipeline stages."""
    e2e: Optional[LatencyPercentiles] = None
    stt: Optional[LatencyPercentiles] = None
    llm: Optional[LatencyPercentiles] = None
    tts: Optional[LatencyPercentiles] = None


class AnalyticsSummary(BaseModel):
    """Analytics summary for a time period."""
    total_calls: int = 0
    completed_calls: int = 0
    failed_calls: int = 0
    total_duration_seconds: float = 0.0
    average_duration_seconds: float = 0.0
    success_rate: float = 0.0
    from_date: Optional[str] = None
    to_date: Optional[str] = None


class CallsByDay(BaseModel):
    """Call count for a single day."""
    date: str
    count: int = 0
