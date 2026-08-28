import unittest

from modules.port_scan import assess_assets


class PortAssessmentTests(unittest.TestCase):
    def test_classifies_monitored_open_ports(self) -> None:
        assets = [
            {
                "ip": "192.168.56.10",
                "hostname": "lab-device",
                "open_ports": [22, 23, 8080],
            }
        ]

        result = assess_assets(assets, {22, 23, 443}, {23})

        self.assertEqual(result[0]["open_ports"], [22, 23])
        self.assertEqual(result[0]["findings"][0]["level"], "info")
        self.assertEqual(result[0]["findings"][1]["level"], "high")


if __name__ == "__main__":
    unittest.main()
