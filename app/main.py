from __future__ import annotations

import json
from dataclasses import asdict
from http.server import BaseHTTPRequestHandler, HTTPServer

from app.engine import evaluate_case
from app.knowledge_base import CLINICAL_RULES, KNOWLEDGE_BASE_VERSION
from app.models import CaseInput, PatientFact


class AppHandler(BaseHTTPRequestHandler):
    def _send(self, code: int, payload: dict):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            return self._send(200, {"status": "ok"})
        if self.path == "/knowledge-base":
            return self._send(
                200,
                {
                    "version": KNOWLEDGE_BASE_VERSION,
                    "rules": [
                        {
                            "id": r.id,
                            "title": r.title,
                            "level": r.level,
                            "fact_key": r.fact_key,
                            "operator": r.operator,
                            "threshold": r.threshold,
                        }
                        for r in CLINICAL_RULES
                    ],
                },
            )
        return self._send(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/evaluate":
            return self._send(404, {"error": "not found"})
        content_len = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(content_len)
        payload = json.loads(raw.decode("utf-8"))
        facts = [PatientFact(**x) for x in payload.get("facts", [])]
        case = CaseInput(
            patient_id=payload["patient_id"],
            encounter_id=payload.get("encounter_id"),
            department=payload.get("department"),
            raw_text=payload.get("raw_text"),
            facts=facts,
        )
        resp = evaluate_case(case)
        return self._send(200, asdict(resp))


def run(host: str = "0.0.0.0", port: int = 8000):
    server = HTTPServer((host, port), AppHandler)
    print(f"server running at http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
