"""BESS AI SDK — Resource classes."""
from bessai.resources.agents import AgentResource, AsyncAgentResource
from bessai.resources.calls import CallsResource, AsyncCallsResource
from bessai.resources.phone_numbers import PhoneNumbersResource, AsyncPhoneNumbersResource
from bessai.resources.batch_calls import BatchCallsResource, AsyncBatchCallsResource
from bessai.resources.workflows import WorkflowsResource, AsyncWorkflowsResource
from bessai.resources.analytics import AnalyticsResource, AsyncAnalyticsResource
from bessai.resources.knowledge_bases import KnowledgeBasesResource, AsyncKnowledgeBasesResource
from bessai.resources.api_keys import APIKeysResource, AsyncAPIKeysResource

# Backward compatibility aliases
AgentsResource = AgentResource
AsyncAgentsResource = AsyncAgentResource

__all__ = [
    "AgentResource", "AsyncAgentResource",
    "AgentsResource", "AsyncAgentsResource",  # compat
    "CallsResource", "AsyncCallsResource",
    "PhoneNumbersResource", "AsyncPhoneNumbersResource",
    "BatchCallsResource", "AsyncBatchCallsResource",
    "WorkflowsResource", "AsyncWorkflowsResource",
    "AnalyticsResource", "AsyncAnalyticsResource",
    "KnowledgeBasesResource", "AsyncKnowledgeBasesResource",
    "APIKeysResource", "AsyncAPIKeysResource",
]
