from __future__ import annotations
from .runtime import Tool

def health(args):
    service = str(args.get("service", "unknown"))
    return {"service": service, "status": "healthy"}

def deployment_risk(args):
    changes = int(args.get("changes", 0))
    critical = int(args.get("critical_findings", 0))
    rollback = bool(args.get("rollback_ready", False))
    score = min(100, changes * 2 + critical * 30 + (0 if rollback else 20))
    return {"risk_score": score, "decision": "block" if critical or score >= 70 else "allow", "reason": "critical finding present" if critical else "policy score"}

DEFAULT_TOOLS = [
    Tool("health", "Check a service health signal", health),
    Tool("deployment_risk", "Evaluate a deployment against a simple policy", deployment_risk),
]
