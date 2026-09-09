# Agent Control Plane

A small, production-minded runtime for **bounded, auditable AI-agent tool execution**.

The idea is simple: LLMs can propose actions, but production systems should decide what is actually allowed to run.

```text
LLM / planner
     |
     v
+-----------------------+
|   Agent Control Plane |
|  allow-list           |
|  max-step budget      |
|  execution trace      |
|  policy checks        |
+----------+------------+
           |
      +----+----+
      |         |
      v         v
   health   deploy-risk
    tool       tool
```

## Why this exists

Agent demos often jump directly from a model response to a powerful tool. This project separates **reasoning from execution**. The runtime accepts a structured plan, validates every requested tool against an allow-list, enforces a bounded step budget, executes tools, and returns an observable trace.

It deliberately uses the Python standard library only: the control-plane concept stays visible instead of being hidden behind an agent framework.

## What it demonstrates

- Explicit tool allow-list: unknown capabilities are denied
- Bounded autonomy with a maximum execution-step budget
- Per-step success/error and latency telemetry
- Deterministic deployment-risk policy tool
- HTTP API and health endpoint
- Non-root Docker image
- Kubernetes deployment with probes, resource limits and dropped Linux capabilities
- Automated tests and GitHub Actions CI

## Run it

Requires Python 3.11+.

```bash
python demo.py
python -m unittest discover -s tests -v
python -m agent_runtime.api
```

Then:

```bash
curl -s http://localhost:8080/v1/execute \
  -H 'content-type: application/json' \
  -d '{
    "plan": [
      {"tool":"health","args":{"service":"checkout"}},
      {"tool":"deployment_risk","args":{
        "changes":8,
        "critical_findings":0,
        "rollback_ready":true
      }}
    ]
  }'
```

## Security property

A planner cannot silently invent a new capability. For example, a request for a `shell` tool is rejected because no such tool is registered. This is intentionally tested.

This is a compact prototype, not a claim of a complete agent sandbox. A production implementation would add authentication/authorization, isolated tool workers, durable traces, timeouts, rate limits, signed policy bundles, OpenTelemetry, secrets brokering and human approval for high-impact actions.

## Next direction

The interesting extension is a Kubernetes-native version where teams register tools and policies declaratively, while the control plane handles identity, approvals, execution and observability across many agents.
