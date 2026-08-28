import unittest

from modules.diff_check import analyze_config_lines


class ConfigDiffTests(unittest.TestCase):
    def test_detects_dangerous_addition_and_control_removal(self) -> None:
        old = ["ip access-list extended MANAGEMENT", " deny ip any any log"]
        new = ["ip access-list extended MANAGEMENT", " permit ip any any"]

        changes, alerts = analyze_config_lines(old, new)

        self.assertEqual(len(changes), 2)
        self.assertIn("- deny ip any any log", alerts)
        self.assertIn("+ permit ip any any", alerts)

    def test_identical_configs_produce_no_changes(self) -> None:
        changes, alerts = analyze_config_lines(["hostname lab"], ["hostname lab"])

        self.assertEqual(changes, [])
        self.assertEqual(alerts, [])


if __name__ == "__main__":
    unittest.main()
