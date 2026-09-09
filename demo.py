from agent_runtime.runtime import AgentRuntime, json_trace
from agent_runtime.tools import DEFAULT_TOOLS

plan = [
    {"tool":"health", "args":{"service":"checkout"}},
    {"tool":"deployment_risk", "args":{"changes":8, "critical_findings":0, "rollback_ready":True}},
]
print(json_trace(AgentRuntime(DEFAULT_TOOLS).execute(plan)))
