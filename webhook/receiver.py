#!/usr/bin/env python3
"""Standard-library webhook bridge for Alertmanager/Grafana to Zabbix."""
from __future__ import annotations
import hmac, json, logging, os, re, subprocess
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

LOG = logging.getLogger("monitoring_webhook")
MAX_BODY_BYTES = int(os.environ.get("MAX_BODY_BYTES", "1048576"))

def normal_state(value: Any) -> int | None:
    if not isinstance(value, str):
        return None
    value = value.strip().lower()
    if value in {"firing", "alerting", "active"}:
        return 1
    if value in {"resolved", "ok", "normal"}:
        return 0
    return None

def payload_to_state(payload: dict[str, Any]) -> int | None:
    if not isinstance(payload, dict):
        return None
    alerts = payload.get("alerts")
    if isinstance(alerts, list) and alerts:
        states, unknown = [], False
        for alert in alerts:
            if not isinstance(alert, dict):
                unknown = True
                continue
            state = normal_state(alert.get("status") or alert.get("state"))
            if state is None:
                unknown = True
            else:
                states.append(state)
        if 1 in states:
            return 1
        if states and not unknown:
            return 0
        # A non-empty alerts array with unknown states is ambiguous. Do not
        # fall back to the summary status and accidentally convert it to recovery.
        return None
    for field in ("status", "state"):
        state = normal_state(payload.get(field))
        if state is not None:
            return state
    return None

def required_env(name: str, default: str | None = None) -> str:
    value = os.environ.get(name, default)
    if value is None or not value.strip():
        raise RuntimeError(f"Required environment variable {name} is not set")
    return value.strip()

def send_zabbix_state(state: int) -> tuple[bool, str]:
    args = [
        required_env("ZABBIX_SENDER_BIN", "/usr/bin/zabbix_sender"),
        "-z", required_env("ZABBIX_SERVER_ADDR", "127.0.0.1"),
        "-p", required_env("ZABBIX_SERVER_PORT", "10051"),
        "-s", required_env("ZABBIX_HOST", "linux-client01"),
        "-k", required_env("ZABBIX_ITEM_KEY", "prometheus.alert.state"),
        "-o", str(state),
    ]
    try:
        result = subprocess.run(args, check=False, capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.TimeoutExpired) as exc:
        LOG.error("zabbix_sender could not complete: %s", type(exc).__name__)
        return False, "zabbix_sender could not complete"
    output = (result.stdout or "") + "\n" + (result.stderr or "")
    positive = re.search(r"processed:\s*1;\s*failed:\s*0(?:\s*;|\s|$)", output, re.I)
    if result.returncode != 0 or not positive:
        LOG.error("zabbix_sender failed (exit=%s)", result.returncode)
        return False, "zabbix_sender did not confirm processing one value"
    LOG.info("zabbix_sender processed one state value (state=%s)", state)
    return True, "processed one state value"

class Handler(BaseHTTPRequestHandler):
    server_version = "MonitoringWebhook/1.0"
    sys_version = ""
    def log_message(self, fmt: str, *args: Any) -> None:
        LOG.info("client=%s " + fmt, self.client_address[0], *args)
    def reply(self, code: int, body: dict[str, Any]) -> None:
        raw = json.dumps(body, separators=(",", ":")).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(raw)
    def do_GET(self) -> None:
        if self.path == "/healthz":
            self.reply(200, {"status": "ok"})
        else:
            self.reply(404, {"error": "not found"})
    def do_POST(self) -> None:
        if self.path not in {"/", "/alertmanager", "/grafana"}:
            self.reply(404, {"error": "not found"})
            return
        expected = os.environ.get("WEBHOOK_TOKEN", "")
        auth = self.headers.get("Authorization", "")
        supplied = auth[7:].strip() if auth.lower().startswith("bearer ") else ""
        if not expected or not supplied or not hmac.compare_digest(supplied, expected):
            self.reply(401, {"error": "unauthorized"})
            return
        if "application/json" not in self.headers.get("Content-Type", "").lower():
            self.reply(415, {"error": "content type must be application/json"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self.reply(400, {"error": "invalid content length"})
            return
        if length <= 0 or length > MAX_BODY_BYTES:
            self.reply(413 if length > MAX_BODY_BYTES else 400, {"error": "invalid body size"})
            return
        try:
            payload = json.loads(self.rfile.read(length))
        except (json.JSONDecodeError, UnicodeDecodeError):
            self.reply(400, {"error": "invalid JSON"})
            return
        state = payload_to_state(payload) if isinstance(payload, dict) else None
        if state is None:
            self.reply(400, {"error": "unrecognized alert state; no Zabbix value sent"})
            return
        ok, message = send_zabbix_state(state)
        if not ok:
            self.reply(502, {"error": message})
            return
        self.reply(200, {"status": "accepted", "state": "firing" if state else "resolved"})

def main() -> None:
    logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO").upper(),
                        format="%(asctime)s %(levelname)s %(name)s %(message)s")
    host = required_env("WEBHOOK_LISTEN_HOST", "127.0.0.1")
    port = int(required_env("WEBHOOK_LISTEN_PORT", "5001"))
    required_env("WEBHOOK_TOKEN")
    sender = required_env("ZABBIX_SENDER_BIN", "/usr/bin/zabbix_sender")
    if not os.path.isfile(sender) or not os.access(sender, os.X_OK):
        raise RuntimeError(f"zabbix_sender is not executable at {sender}")
    required_env("ZABBIX_HOST", "linux-client01")
    required_env("ZABBIX_ITEM_KEY", "prometheus.alert.state")
    server = ThreadingHTTPServer((host, port), Handler)
    LOG.info("listening on %s:%s", host, port)
    try:
        server.serve_forever(poll_interval=0.5)
    finally:
        server.server_close()
        LOG.info("server stopped")

if __name__ == "__main__":
    main()
