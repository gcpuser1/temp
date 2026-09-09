import unittest
from agent_runtime.runtime import AgentRuntime, PolicyError
from agent_runtime.tools import DEFAULT_TOOLS

class RuntimeTests(unittest.TestCase):
    def setUp(self): self.runtime = AgentRuntime(DEFAULT_TOOLS, max_steps=2)
    def test_executes_allowlisted_tool(self):
        result = self.runtime.execute([{"tool":"health","args":{"service":"payments"}}])
        self.assertTrue(result["ok"]); self.assertEqual(result["steps"][0]["output"]["status"], "healthy"); self.assertTrue(result["trace_id"])
    def test_blocks_unknown_tool(self):
        with self.assertRaises(PolicyError): self.runtime.execute([{"tool":"shell","args":{"cmd":"rm -rf /"}}])
    def test_bounds_agent_steps(self):
        with self.assertRaises(PolicyError): self.runtime.execute([{"tool":"health","args":{}}] * 3)
    def test_deployment_policy_blocks_critical(self):
        result = self.runtime.execute([{"tool":"deployment_risk","args":{"changes":2,"critical_findings":1,"rollback_ready":True}}])
        self.assertEqual(result["steps"][0]["output"]["decision"], "block")

if __name__ == "__main__": unittest.main()
