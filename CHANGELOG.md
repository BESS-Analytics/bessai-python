# Changelog

All notable changes to the BESS AI Python SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
