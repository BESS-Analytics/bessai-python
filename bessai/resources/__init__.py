"""BESS AI SDK — Resource classes."""
from bessai.resources.agents import AgentResource, AsyncAgentResource
from bessai.resources.calls import CallResource, AsyncCallResource
from bessai.resources.phone_numbers import PhoneNumberResource, AsyncPhoneNumberResource
from bessai.resources.batch_calls import BatchCallResource, AsyncBatchCallResource
from bessai.resources.workflows import WorkflowResource, AsyncWorkflowResource
from bessai.resources.analytics import AnalyticsResource, AsyncAnalyticsResource
from bessai.resources.knowledge_bases import KnowledgeBasesResource, AsyncKnowledgeBasesResource
from bessai.resources.api_keys import APIKeysResource, AsyncAPIKeysResource

# Backward compatibility aliases
AgentsResource = AgentResource
AsyncAgentsResource = AsyncAgentResource
CallsResource = CallResource
AsyncCallsResource = AsyncCallResource
PhoneNumbersResource = PhoneNumberResource
AsyncPhoneNumbersResource = AsyncPhoneNumberResource
BatchCallsResource = BatchCallResource
AsyncBatchCallsResource = AsyncBatchCallResource
WorkflowsResource = WorkflowResource
AsyncWorkflowsResource = AsyncWorkflowResource

__all__ = [
    "AgentResource", "AsyncAgentResource",
    "AgentsResource", "AsyncAgentsResource",  # compat
    "CallResource", "AsyncCallResource",
    "CallsResource", "AsyncCallsResource",  # compat
    "PhoneNumberResource", "AsyncPhoneNumberResource",
    "PhoneNumbersResource", "AsyncPhoneNumbersResource",  # compat
    "BatchCallResource", "AsyncBatchCallResource",
    "BatchCallsResource", "AsyncBatchCallsResource",  # compat
    "WorkflowResource", "AsyncWorkflowResource",
    "WorkflowsResource", "AsyncWorkflowsResource",  # compat
    "AnalyticsResource", "AsyncAnalyticsResource",
    "KnowledgeBasesResource", "AsyncKnowledgeBasesResource",
    "APIKeysResource", "AsyncAPIKeysResource",
]
