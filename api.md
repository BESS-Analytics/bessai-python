# BESS AI Python SDK — API Reference

> Every sync method has an identical `async` mirror on the `AsyncBessAI` client.
> Access resources via the singular accessor (e.g. `client.agent`).
> Plural aliases (e.g. `client.agents`) are provided for backward compatibility.

---

## Client

```python
from bessai import BessAI, AsyncBessAI

# Sync
client = BessAI(api_key="bess_sk_live_...")

# Async
client = AsyncBessAI(api_key="bess_sk_live_...")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | `str \| None` | `BESSAI_API_KEY` env var | API key for authentication |
| `base_url` | `str \| None` | `BESSAI_BASE_URL` env var or `https://api.bessai.com` | API base URL |
| `timeout` | `float` | `30.0` | Request timeout in seconds |
| `max_retries` | `int` | `3` | Max retries for transient errors (429, 5xx) |

---

## Agent — `client.agent`

### `create(**kwargs) -> AgentResponse`

Create a new voice AI agent.

### `retrieve(agent_id: str) -> AgentResponse`

Get an agent by ID, including all version history.

### `list(skip: int = 0, limit: int = 20) -> List[AgentResponse]`

List all agents for the current organization.

### `update(agent_id: str, **kwargs) -> AgentResponse`

Update agent configuration.

### `delete(agent_id: str) -> None`

Permanently delete an agent and all its versions.

### `publish(agent_id: str) -> AgentResponse`

Publish the current draft as a new live version.

### `get_versions(agent_id: str) -> List[AgentVersion]`

Get the full version history of an agent.

### `export(agent_id: str) -> Dict[str, Any]`

Export an agent as a portable JSON object.

### `import_agent(file_path: str) -> AgentResponse`

Import an agent from a previously exported JSON file.

### `link_workflow(agent_id: str, workflow_id: str, **kwargs) -> AgentWorkflowLinkResponse`

Link a workflow to this agent.

### `unlink_workflow(agent_id: str, workflow_id: str) -> Dict[str, Any]`

Remove a workflow link from this agent.

### `list_workflows(agent_id: str) -> List[AgentWorkflowListItem]`

Get all workflows linked to an agent.

---

## Call — `client.call`

### `create_phone_call(**kwargs) -> CallResponse`

Create an outbound phone call via SIP trunk.

### `create_web_call(**kwargs) -> CallResponse`

Create a browser-to-agent call via WebRTC.

### `create_test_call(**kwargs) -> CallResponse`

Create a test call for development and agent testing.

### `retrieve(call_id: str) -> CallResponse`

Get full call details including transcript, analytics, and recordings.

### `list(skip=0, limit=20, agent_id=None, status=None, call_type=None, batch_call_id=None, from_date=None, to_date=None) -> List[CallListItem]`

List calls with optional filters.

### `end(call_id: str) -> Dict[str, Any]`

End an active call.

### `delete(call_id: str) -> None`

Delete a call record.

---

## Phone Number — `client.phone_number`

### `create(**kwargs) -> PhoneNumberResponse`

Register a phone number.

### `retrieve(phone_number_id: str) -> PhoneNumberDetailResponse`

Get a phone number by ID (includes SIP connections and dispatch rules).

### `list(skip: int = 0, limit: int = 50) -> List[PhoneNumberResponse]`

List all phone numbers for the organization.

### `update(phone_number_id: str, **kwargs) -> PhoneNumberResponse`

Update a phone number's configuration.

### `delete(phone_number_id: str) -> None`

Delete a phone number and its SIP connections.

### `update_agents(phone_number_id: str, *, inbound_agent_id=None, outbound_agent_id=None) -> PhoneNumberResponse`

Quick-update inbound/outbound agent assignments.

### `create_sip_connection(phone_number_id: str, **kwargs) -> SIPConnectionResponse`

Create a SIP connection and auto-sync to LiveKit.

### `list_sip_connections(phone_number_id: str) -> List[SIPConnectionResponse]`

List all SIP connections for a phone number.

### `retrieve_sip_connection(phone_number_id: str, connection_id: str) -> SIPConnectionResponse`

Get a single SIP connection by ID.

### `update_sip_connection(phone_number_id: str, connection_id: str, **kwargs) -> SIPConnectionResponse`

Update a SIP connection and re-sync to LiveKit.

### `delete_sip_connection(phone_number_id: str, connection_id: str) -> None`

Delete a SIP connection and clean up LiveKit resources.

### `sync_sip_connection(phone_number_id: str, connection_id: str) -> SIPConnectionResponse`

Force re-sync a SIP connection with LiveKit.

---

## Batch Call — `client.batch_call`

### `create(**kwargs) -> BatchCallStatusResponse`

Create a batch call campaign.

### `retrieve(batch_call_id: str) -> BatchCallStatusResponse`

Get real-time batch call status with detailed counts.

### `list(skip=0, limit=20, status=None) -> List[BatchCallResponse]`

List batch call campaigns.

### `list_active() -> List[BatchCallStatusResponse]`

List only active (non-terminal) batch calls with real-time counts.

### `list_items(batch_call_id: str, status=None, limit=100) -> List[BatchCallItemResponse]`

Get individual contact results for a batch call.

### `delete(batch_call_id: str) -> None`

Delete a batch call campaign (only if not running).

### `start(batch_call_id: str) -> BatchCallStatusResponse`

Start or resume a batch call campaign.

### `pause(batch_call_id: str) -> BatchCallStatusResponse`

Pause a running batch. Active calls complete; no new calls initiated.

### `resume(batch_call_id: str) -> BatchCallStatusResponse`

Resume a paused batch call campaign.

### `cancel(batch_call_id: str) -> BatchCallStatusResponse`

Cancel a batch call. Pending items are marked as cancelled.

---

## Workflow — `client.workflow`

### `create(**kwargs) -> GenerateResponse`

AI-generate a workflow from a natural-language description.

### `refine(workflow_id: str, **kwargs) -> GenerateResponse`

Refine an existing workflow with AI based on feedback.

### `retrieve(workflow_id: str) -> WorkflowDetailResponse`

Get a workflow by ID with full detail.

### `list(trigger_type=None, status=None, agent_id=None, include_deleted=False, page=1, per_page=20) -> List[WorkflowResponse]`

List workflows with filtering and pagination.

### `update(workflow_id: str, **kwargs) -> WorkflowDetailResponse`

Update workflow settings.

### `delete(workflow_id: str, hard: bool = False) -> Dict[str, Any]`

Delete a workflow (soft-delete by default).

### `restore(workflow_id: str) -> Dict[str, Any]`

Restore a soft-deleted workflow to draft status.

### `save_secrets(workflow_id: str, **kwargs) -> Dict[str, Any]`

Encrypt and save credentials for Runtime Injection.

### `get_credential_schema(credential_type: str) -> CredentialSchemaResponse`

Get the required field schema for an n8n credential type.

### `deploy(workflow_id: str) -> DeployResponse`

Deploy a workflow to n8n and activate it.

### `test(workflow_id: str, test_data=None) -> ExecuteResponse`

Test-execute a workflow with sample call data.

### `execute(workflow_id: str, **kwargs) -> ExecuteResponse`

Manually trigger a workflow execution.

### `list_executions(workflow_id: str, status=None, page=1, per_page=20) -> Dict[str, Any]`

Get execution history for a workflow.

### `export(workflow_id: str) -> Dict[str, Any]`

Export a workflow as a portable JSON object.

### `import_workflow(file_path: str) -> Dict[str, Any]`

Import a workflow from a previously exported JSON file.

### `link_agent(workflow_id: str, agent_id: str, **kwargs) -> AgentWorkflowLinkResponse`

Link a workflow to an agent with optional trigger conditions.

### `update_agent_link(workflow_id: str, agent_id: str, **kwargs) -> AgentWorkflowLinkResponse`

Update an agent-workflow link's configuration.

### `unlink_agent(workflow_id: str, agent_id: str) -> Dict[str, Any]`

Remove a workflow-agent link.

### `list_agents(workflow_id: str) -> List[AgentWorkflowLinkResponse]`

Get all agents linked to a workflow.

### `list_by_agent(agent_id: str) -> List[AgentWorkflowListItem]`

Get all workflows linked to an agent.

### `set_schedule(workflow_id: str, cron=None, interval_minutes=None, timezone="UTC") -> Dict[str, Any]`

Set or update a workflow's schedule.

### `remove_schedule(workflow_id: str) -> Dict[str, Any]`

Remove a workflow from the schedule.

### `get_schedule(workflow_id: str) -> ScheduleStatusResponse`

Get a workflow's current schedule status.

### `list_schedules() -> Dict[str, Any]`

List all currently scheduled workflows.

---

## Analytics — `client.analytic`

### `get_summary(from_date=None, to_date=None, agent_id=None) -> AnalyticsSummary`

Get analytics summary for a time period.

### `get_latency(from_date=None, to_date=None, agent_id=None) -> LatencyMetrics`

Get latency percentile metrics across pipeline stages.

### `get_calls_by_day(days: int = 30, agent_id=None) -> List[CallsByDay]`

Get call counts grouped by day.

---

## Billing — `client.billing`

### `get_balance() -> CreditBalanceResponse`

Get current credit balance for the organisation.

### `check_balance(required: float = 0.0) -> BalanceCheckResponse`

Check whether the balance is sufficient for an estimated cost.

### `list_transactions(transaction_type=None, limit=50, offset=0) -> TransactionListResponse`

List credit-ledger transactions.

### `list_usage(event_type=None, reference_id=None, start_date=None, end_date=None, limit=50, offset=0) -> UsageListResponse`

List usage events with optional filters.

### `get_usage_summary(start_date=None, end_date=None) -> UsageSummaryResponse`

Get aggregated usage summary for a date range.

### `get_daily_usage(days: int = 30) -> List[DailyUsageItem]`

Get daily aggregated usage for charting.

### `get_call_usage(call_id: str) -> CallUsageResponse`

Get all usage events for a specific call.

### `get_pricing() -> ServicePricingResponse`

Get all available service pricing.

### `estimate_pricing(agent_type=None, stt_provider=None, stt_model=None, llm_provider=None, llm_model=None, voice_provider=None, realtime_provider=None, realtime_model=None) -> PricingEstimateResponse`

Estimate per-minute pricing for an agent configuration.

---

## Config — `client.config`

### `get_providers() -> ProviderConfig`

Get the complete provider configuration (STT, LLM, TTS, etc.).

### `get_provider(provider_type: str) -> Dict[str, Any]`

Get providers for a specific type (e.g. `"stt"`, `"llm"`, `"tts"`).

### `get_defaults() -> Dict[str, Any]`

Get default configuration values.

### `get_languages() -> List[Any]`

Get list of supported languages.

---

## Knowledge Bases — `client.knowledge_bases`

### `create(**kwargs) -> KnowledgeBase`

Create a knowledge base.

### `list(skip: int = 0, limit: int = 20) -> List[KnowledgeBase]`

List knowledge bases.

### `get(kb_id: str) -> KnowledgeBase`

Get knowledge base details.

### `delete(kb_id: str) -> None`

Delete a knowledge base.

### `upload_document(kb_id: str, file_path: str, filename=None) -> Document`

Upload a document to a knowledge base.

### `delete_document(kb_id: str, document_id: str) -> None`

Delete a document from a knowledge base.

---

## API Keys — `client.api_keys`

### `create(**kwargs) -> APIKeyCreated`

Create a new API key. The full key is only returned once.

### `list(skip=0, limit=20, include_inactive=False) -> List[APIKey]`

List API keys (masked).

### `get(key_id: str) -> APIKey`

Get API key details.

### `update(key_id: str, **kwargs) -> APIKey`

Update API key name, scopes, or settings.

### `delete(key_id: str) -> None`

Revoke an API key immediately.

### `rotate(key_id: str, grace_period_hours: int = 24) -> APIKeyCreated`

Rotate an API key with a grace period for the old key.

### `get_usage(key_id: str) -> APIKeyUsage`

Get usage statistics for an API key.

---

## Error Handling

```python
from bessai import BessAI, AuthenticationError, RateLimitError, NotFoundError

client = BessAI()

try:
    agent = client.agent.retrieve("agent_abc123")
except AuthenticationError:
    print("Invalid or missing API key")
except NotFoundError:
    print("Agent not found")
except RateLimitError as e:
    print(f"Rate limited — retry after {e.retry_after}s")
```

### Exception Hierarchy

| Exception | HTTP Status | Description |
|-----------|-------------|-------------|
| `BessAIError` | — | Base exception for all SDK errors |
| `AuthenticationError` | 401 | Invalid or missing API key |
| `PermissionDeniedError` | 403 | Insufficient scope or not an admin |
| `NotFoundError` | 404 | Resource does not exist |
| `ValidationError` | 422 | Request body failed validation |
| `RateLimitError` | 429 | Rate limit exceeded |
| `InternalServerError` | 500 | Server-side error |
| `ConnectionError` | — | Network connectivity issue |
| `TimeoutError` | — | Request timed out |
