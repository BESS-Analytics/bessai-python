# Changelog

All notable changes to the BESS AI Python SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-07-08

### Added

- New `chat` resource module — text chat sessions over the same agent brain as voice
  (`docs/CHAT_AGENTS_SPEC.md`):
  - `create(agent_id=..., transport="rest"|"livekit", channel_type=..., dynamic_variables=..., external_user_key=...)` — `POST /v1/chat/sessions`
  - `create_test_session(agent_id=..., temp_config=..., dynamic_variables=...)` — `POST /v1/chat/test` (mirrors `call.create_test_call`; accepts draft agents)
  - `send_message(session_id, content)` — `POST /v1/chat/sessions/{id}/messages` (REST transport only)
  - `retrieve(session_id, skip=0, limit=50)` — `GET /v1/chat/sessions/{id}` (detail + paginated messages)
  - `list(skip=0, limit=20, agent_id=None, status=None, channel_type=None, from_date=None, to_date=None)` — `GET /v1/chat/sessions`
  - `close(session_id)` — `POST /v1/chat/sessions/{id}/close`
- New types: `ChatSession`, `ChatSessionDetail`, `ChatMessage`, `ChatTurnResult`,
  `ChatSessionCloseResult`, `ChatSessionCreateParams`, `ChatMessageCreateParams`,
  `ChatTestSessionCreateParams`.
- Both `BessAI` and `AsyncBessAI` expose the namespace as `client.chat`.

## [0.1.0] - 2026-03-07

### Added

- Initial release of the BESS AI Python SDK
- Sync (`BessAI`) and async (`AsyncBessAI`) clients
- Resource modules:
  - `agent` — Create, list, retrieve, update, delete, publish agents
  - `call` — Create phone/web/test calls, list, retrieve, end, delete
  - `phone_number` — CRUD for phone numbers with SIP connections
  - `batch_call` — Create and manage batch call campaigns
  - `workflow` — Generate, deploy, execute, and manage workflows
  - `analytic` — Get call analytics summaries, latency, daily breakdowns
  - `billing` — Credit balance, usage tracking, pricing, transactions
  - `config` — Provider configurations, defaults, supported languages
  - `knowledge_bases` — CRUD for knowledge bases and document uploads
  - `api_keys` — Create, rotate, revoke, and manage API keys
- Automatic retry with exponential backoff for transient errors (429, 5xx)
- Typed request parameters and Pydantic response models
- Exception hierarchy: `AuthenticationError`, `RateLimitError`, `NotFoundError`, etc.
- WebSocket streaming for real-time batch call status updates
- Environment variable support (`BESSAI_API_KEY`, `BESSAI_BASE_URL`)
- `py.typed` marker for PEP 561 type-checking support
