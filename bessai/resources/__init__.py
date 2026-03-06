"""BESS AI SDK — Resource classes."""
from bessai.resources.agents import AgentResource, AsyncAgentResource
from bessai.resources.calls import CallResource, AsyncCallResource
from bessai.resources.phone_numbers import PhoneNumbersResource, AsyncPhoneNumbersResource
from bessai.resources.batch_calls import BatchCallsResource, AsyncBatchCallsResource
from bessai.resources.workflows import WorkflowsResource, AsyncWorkflowsResource
from bessai.resources.analytics import AnalyticsResource, AsyncAnalyticsResource
from bessai.resources.knowledge_bases import KnowledgeBasesResource, AsyncKnowledgeBasesResource
from bessai.resources.api_keys import APIKeysResource, AsyncAPIKeysResource

# Backward compatibility aliases
AgentsResource = AgentResource
AsyncAgentsResource = AsyncAgentResource
CallsResource = CallResource
AsyncCallsResource = AsyncCallResource

__all__ = [
    "AgentResource", "AsyncAgentResource",
    "AgentsResource", "AsyncAgentsResource",  # compat
    "CallResource", "AsyncCallResource",
    "CallsResource", "AsyncCallsResource",  # compat
    "PhoneNumbersResource", "AsyncPhoneNumbersResource",
    "BatchCallsResource", "AsyncBatchCallsResource",
    "WorkflowsResource", "AsyncWorkflowsResource",
    "AnalyticsResource", "AsyncAnalyticsResource",
    "KnowledgeBasesResource", "AsyncKnowledgeBasesResource",
    "APIKeysResource", "AsyncAPIKeysResource",
]
