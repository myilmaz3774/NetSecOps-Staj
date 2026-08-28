import unittest

from modules.notifier import format_alerts
from modules.workflow import build_summary


class WorkflowTests(unittest.TestCase):
    def test_builds_expected_summary(self) -> None:
        assets = [{"ip": "192.168.56.10"}, {"ip": "192.168.56.20"}]
        port_results = [
            {
                "open_ports": [21, 443],
                "findings": [
                    {"level": "high"},
                    {"level": "info"},
                ],
            }
        ]

        summary = build_summary(assets, port_results, ["+ permit ip any any"])

        self.assertEqual(summary["asset_count"], 2)
        self.assertEqual(summary["open_port_count"], 2)
        self.assertEqual(summary["high_risk_count"], 1)
        self.assertEqual(summary["critical_config_change_count"], 1)

    def test_formats_empty_and_populated_alerts(self) -> None:
        self.assertEqual(format_alerts([]), "Kritik değişiklik tespit edilmedi.")
        self.assertIn("permit ip any any", format_alerts(["+ permit ip any any"]))


if __name__ == "__main__":
    unittest.main()
