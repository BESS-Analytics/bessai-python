"""Batch call types for the BESS AI SDK."""
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------------
# Contact (input for batch creation)
# ---------------------------------------------------------------------------

class BatchCallContact(BaseModel):
    """Single contact entry for a batch call campaign."""

    phone_number: str
    dynamic_variables: Optional[Dict[str, Any]] = None


# ---------------------------------------------------------------------------
# Create params
# ---------------------------------------------------------------------------

class BatchCallCreateParams(BaseModel):
    """Parameters for creating a batch call campaign.

    Example::

        params = BatchCallCreateParams(
            agent_id="ag_abc123",
            from_number="+905551234567",
            name="March Outreach",
            contacts=[
                BatchCallContact(phone_number="+12125551001"),
                BatchCallContact(
                    phone_number="+12125551002",
                    dynamic_variables={"name": "Alice", "company": "ACME"},
                ),
            ],
            max_concurrent_calls=10,
            retry_attempts=2,
        )
    """

    agent_id: str
    from_number: str
    contacts: List[BatchCallContact]
    max_concurrent_calls: int = 5
    retry_attempts: int = 1
    name: Optional[str] = None

    def to_api_params(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)


# ---------------------------------------------------------------------------
# Response — list view (returned by list())
# ---------------------------------------------------------------------------

class BatchCallResponse(BaseModel):
    """Batch call campaign returned by the list endpoint."""

    model_config = ConfigDict(populate_by_name=True)

    batch_call_id: str = Field(alias="id")
    name: str = ""
    agent_id: str = ""
    from_number: str = ""

    # Counts
    total_count: int = 0
    completed_count: int = 0
    failed_count: int = 0

    # Config
    max_concurrent: int = 5
    retry_attempts: int = 1

    # Status
    status: str = "pending"
    progress_percent: float = 0.0

    # Timestamps
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    created_at: Optional[str] = None


# ---------------------------------------------------------------------------
# Response — status view (returned by retrieve / start / pause / resume / cancel)
# ---------------------------------------------------------------------------

class BatchCallStatusResponse(BaseModel):
    """Real-time batch call status with detailed counts."""

    model_config = ConfigDict(populate_by_name=True)

    batch_call_id: str = Field(alias="id")
    name: Optional[str] = None
    status: str = "pending"

    # Summary counts
    total: int = 0
    pending: int = 0
    active: int = 0
    completed: int = 0
    failed: int = 0
    processed: int = 0

    # Detailed per-status counts
    counts: Dict[str, int] = Field(default_factory=dict)

    # Progress
    progress_percent: float = 0.0

    # Timestamps
    started_at: Optional[str] = None
    completed_at: Optional[str] = None


# ---------------------------------------------------------------------------
# Batch call item (individual contact result)
# ---------------------------------------------------------------------------

class BatchCallItemResponse(BaseModel):
    """Individual contact result within a batch call campaign."""

    model_config = ConfigDict(populate_by_name=True)

    item_id: str = Field(alias="id")
    phone_number: str
    status: str = "pending"
    attempt_count: int = 0
    call_id: Optional[str] = None
    error_message: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None


# ---------------------------------------------------------------------------
# Backward-compatibility aliases
# ---------------------------------------------------------------------------
BatchCall = BatchCallResponse
BatchCallCreate = BatchCallCreateParams
BatchCallItem = BatchCallItemResponse
