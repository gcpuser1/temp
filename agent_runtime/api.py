from __future__ import annotations
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json, os
from .runtime import AgentRuntime, PolicyError
from .tools import DEFAULT_TOOLS

runtime = AgentRuntime(DEFAULT_TOOLS, max_steps=int(os.getenv("MAX_AGENT_STEPS", "4")))

class Handler(BaseHTTPRequestHandler):
    def _send(self, status, payload):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def do_GET(self):
        self._send(200, {"status":"ok"}) if self.path == "/healthz" else self._send(404, {"error":"not found"})
    def do_POST(self):
        if self.path != "/v1/execute":
            return self._send(404, {"error":"not found"})
        try:
            length = int(self.headers.get("content-length", "0"))
            payload = json.loads(self.rfile.read(length) or b"{}")
            self._send(200, runtime.execute(payload.get("plan", [])))
        except (ValueError, json.JSONDecodeError, PolicyError) as exc:
            self._send(400, {"error":str(exc)})
    def log_message(self, fmt, *args):
        return

def main():
    port = int(os.getenv("PORT", "8080"))
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print(f"agent runtime listening on :{port}", flush=True)
    server.serve_forever()

if __name__ == "__main__":
    main()
