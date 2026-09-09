from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Any
import json, time, uuid

@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    fn: Callable[[dict[str, Any]], dict[str, Any]]

class PolicyError(Exception):
    pass

class AgentRuntime:
    """Tiny, auditable agent runtime with allow-listed tools and bounded execution."""

    def __init__(self, tools: list[Tool], max_steps: int = 4):
        self.tools = {t.name: t for t in tools}
        self.max_steps = max_steps

    def execute(self, plan: list[dict[str, Any]]) -> dict[str, Any]:
        trace_id = str(uuid.uuid4())
        started = time.perf_counter()
        events = []
        if len(plan) > self.max_steps:
            raise PolicyError(f"plan has {len(plan)} steps; max_steps={self.max_steps}")
        for i, step in enumerate(plan, start=1):
            name = step.get("tool")
            if name not in self.tools:
                raise PolicyError(f"tool not allowed: {name}")
            args = step.get("args", {})
            t0 = time.perf_counter()
            try:
                output = self.tools[name].fn(args)
                events.append({"step": i, "tool": name, "ok": True, "latency_ms": round((time.perf_counter()-t0)*1000, 2), "output": output})
            except Exception as exc:
                events.append({"step": i, "tool": name, "ok": False, "latency_ms": round((time.perf_counter()-t0)*1000, 2), "error": str(exc)})
                break
        return {"trace_id": trace_id, "ok": all(e["ok"] for e in events), "steps": events, "total_latency_ms": round((time.perf_counter()-started)*1000, 2)}

def json_trace(result: dict[str, Any]) -> str:
    return json.dumps(result, indent=2, sort_keys=True)
