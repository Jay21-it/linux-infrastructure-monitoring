import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "webhook"))
from receiver import payload_to_state  # noqa: E402

class PayloadStateTests(unittest.TestCase):
    def test_alertmanager_firing(self):
        self.assertEqual(payload_to_state({"status": "firing", "alerts": [{"status": "firing"}]}), 1)
    def test_alertmanager_resolved(self):
        self.assertEqual(payload_to_state({"status": "resolved", "alerts": [{"status": "resolved"}]}), 0)
    def test_grafana_alerting(self):
        self.assertEqual(payload_to_state({"state": "alerting", "alerts": [{"status": "firing"}]}), 1)
    def test_grafana_ok(self):
        self.assertEqual(payload_to_state({"state": "ok", "alerts": [{"status": "resolved"}]}), 0)
    def test_any_firing_keeps_group_active(self):
        self.assertEqual(payload_to_state({"status": "firing", "alerts": [{"status": "resolved"}, {"status": "firing"}]}), 1)
    def test_no_data_is_not_recovery(self):
        self.assertIsNone(payload_to_state({"state": "no_data", "alerts": [{"status": "no_data"}]}))
    def test_unknown_payload_rejected(self):
        self.assertIsNone(payload_to_state({"message": "not an alert"}))
        self.assertIsNone(payload_to_state([]))

    def test_unknown_nested_state_is_not_overridden_by_resolved_summary(self):
        payload = {
            "status": "resolved",
            "alerts": [{"status": "no_data"}],
        }
        self.assertIsNone(payload_to_state(payload))

    def test_empty_alerts_can_use_top_level_status(self):
        self.assertEqual(payload_to_state({"status": "resolved", "alerts": []}), 0)

if __name__ == "__main__":
    unittest.main()
