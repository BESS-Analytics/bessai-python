# BESS AI Python SDK

Official Python SDK for the [BESS AI](https://bessai.com) Voice Platform.

## Installation

```bash
pip install bessai
```

## Quick Start

```python
from bessai import BessAI

client = BessAI(api_key="bess_sk_live_a1b2c3d4...")

# Create an agent
agent = client.agents.create(
    name="Customer Support",
    llm_provider="openai",
    llm_model="gpt-4o",
    system_prompt="You are a helpful customer support agent.",
    voice_provider="elevenlabs",
    voice_id="21m00Tcm4TlvDq8ikWAM",
    language="en-US",
)

# Make a phone call
call = client.calls.create_phone_call(
    agent_id=agent.id,
    from_number="+14157774444",
    to_number="+12137774445",
    metadata={"customer_id": "cust_123"},
)

print(call.id)
print(call.status)
```

## Async Usage

```python
from bessai import AsyncBessAI

async def main():
    async with AsyncBessAI(api_key="bess_sk_live_...") as client:
        agents = await client.agents.list()
        for agent in agents:
            print(agent.name)

        # Stream batch call status
        async with client.streaming.batch_call_status("campaign-id") as stream:
            async for event in stream:
                print(event)
```

## Configuration

```python
# From environment variable
import os
os.environ["BESSAI_API_KEY"] = "bess_sk_live_..."
client = BessAI()  # Reads from BESSAI_API_KEY

# Custom base URL (self-hosted)
client = BessAI(
    api_key="bess_sk_live_...",
    base_url="https://your-instance.example.com",
    timeout=60.0,
    max_retries=5,
)
```

## Resources

| Resource | Methods |
|----------|---------|
| `client.agents` | `create`, `list`, `get`, `update`, `delete`, `publish`, `list_versions` |
| `client.calls` | `create_phone_call`, `create_web_call`, `list`, `get`, `end`, `delete` |
| `client.phone_numbers` | `create`, `list`, `get`, `update`, `delete` |
| `client.batch_calls` | `create`, `list`, `get`, `get_status`, `get_items`, `start`, `pause`, `resume`, `cancel`, `delete` |
| `client.workflows` | `generate`, `list`, `get`, `update`, `delete`, `deploy`, `execute`, `test` |
| `client.analytics` | `get_summary`, `get_latency`, `get_calls_by_day` |
| `client.knowledge_bases` | `create`, `list`, `get`, `delete`, `upload_document`, `delete_document` |
| `client.api_keys` | `create`, `list`, `get`, `update`, `delete`, `rotate`, `get_usage` |

## Error Handling

```python
from bessai import BessAI, AuthenticationError, RateLimitError, NotFoundError

client = BessAI(api_key="bess_sk_live_...")

try:
    agent = client.agents.get("invalid-id")
except AuthenticationError:
    print("Invalid API key")
except RateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after}s")
except NotFoundError:
    print("Agent not found")
```

## API Key Management

```python
# Create a scoped API key
key = client.api_keys.create(
    name="CI/CD Pipeline",
    scopes=["agents:read", "calls:write"],
    expires_in_days=90,
    rate_limit_tier="professional",
)
print(key.key)  # Only shown once!

# Rotate a key with 24h grace period
new_key = client.api_keys.rotate(key.id, grace_period_hours=24)
```

## Requirements

- Python >= 3.8
- httpx >= 0.24.0
- pydantic >= 2.0.0
- websockets >= 11.0

## License

MIT
