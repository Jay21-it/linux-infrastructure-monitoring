import json
import os
import sys
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "webhook"))
import receiver  # noqa: E402


class WebhookHTTPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = receiver.ThreadingHTTPServer(("127.0.0.1", 0), receiver.Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def request(self, method, path, payload=None, token=None, content_type="application/json"):
        data = None if payload is None else json.dumps(payload).encode("utf-8")
        headers = {}
        if data is not None:
            headers["Content-Type"] = content_type
        if token is not None:
            headers["Authorization"] = f"Bearer {token}"
        req = urllib.request.Request(self.base_url + path, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=3) as resp:
                return resp.status, json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            return exc.code, json.loads(exc.read().decode("utf-8"))

    def test_health_endpoint(self):
        status, body = self.request("GET", "/healthz")
        self.assertEqual(status, 200)
        self.assertEqual(body["status"], "ok")

    def test_post_requires_bearer_token(self):
        with patch.dict(os.environ, {"WEBHOOK_TOKEN": "test-secret"}):
            with patch.object(receiver, "send_zabbix_state") as sender:
                status, body = self.request("POST", "/alertmanager", {"status": "firing"})
        self.assertEqual(status, 401)
        self.assertEqual(body["error"], "unauthorized")
        sender.assert_not_called()

    def test_firing_state_is_forwarded(self):
        payload = {"status": "firing", "alerts": [{"status": "firing"}]}
        with patch.dict(os.environ, {"WEBHOOK_TOKEN": "test-secret"}):
            with patch.object(receiver, "send_zabbix_state", return_value=(True, "ok")) as sender:
                status, body = self.request("POST", "/alertmanager", payload, token="test-secret")
        self.assertEqual(status, 200)
        self.assertEqual(body["state"], "firing")
        sender.assert_called_once_with(1)

    def test_resolved_state_is_forwarded(self):
        payload = {"status": "resolved", "alerts": [{"status": "resolved"}]}
        with patch.dict(os.environ, {"WEBHOOK_TOKEN": "test-secret"}):
            with patch.object(receiver, "send_zabbix_state", return_value=(True, "ok")) as sender:
                status, body = self.request("POST", "/alertmanager", payload, token="test-secret")
        self.assertEqual(status, 200)
        self.assertEqual(body["state"], "resolved")
        sender.assert_called_once_with(0)

    def test_ambiguous_alert_does_not_send_recovery(self):
        payload = {"status": "resolved", "alerts": [{"status": "no_data"}]}
        with patch.dict(os.environ, {"WEBHOOK_TOKEN": "test-secret"}):
            with patch.object(receiver, "send_zabbix_state") as sender:
                status, body = self.request("POST", "/alertmanager", payload, token="test-secret")
        self.assertEqual(status, 400)
        sender.assert_not_called()


if __name__ == "__main__":
    unittest.main()
