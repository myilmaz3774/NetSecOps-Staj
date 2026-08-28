import ipaddress
import unittest

from modules.validation import validate_assets, validate_settings


class ValidationTests(unittest.TestCase):
    def test_valid_settings_return_network(self) -> None:
        settings = {
            "project_name": "Lab",
            "allowed_network": "192.168.56.0/24",
            "ports": [22, 23],
            "high_risk_ports": [23],
        }

        network = validate_settings(settings)

        self.assertEqual(network, ipaddress.ip_network("192.168.56.0/24"))

    def test_rejects_asset_outside_allowed_network(self) -> None:
        assets = [
            {
                "ip": "10.10.10.10",
                "mac": "00:1A:2B:3C:4D:10",
                "hostname": "outside-device",
                "open_ports": [22],
            }
        ]

        with self.assertRaisesRegex(ValueError, "CIDR kapsamı dışında"):
            validate_assets(assets, ipaddress.ip_network("192.168.56.0/24"))

    def test_rejects_invalid_mac_address(self) -> None:
        assets = [
            {
                "ip": "192.168.56.10",
                "mac": "INVALID",
                "hostname": "lab-device",
                "open_ports": [22],
            }
        ]

        with self.assertRaisesRegex(ValueError, "MAC adresi geçersiz"):
            validate_assets(assets, ipaddress.ip_network("192.168.56.0/24"))


if __name__ == "__main__":
    unittest.main()
