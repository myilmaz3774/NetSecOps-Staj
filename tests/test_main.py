import unittest
from unittest.mock import patch

from main import execute_safely


class MainErrorHandlingTests(unittest.TestCase):
    @patch("builtins.print")
    def test_reports_expected_error_without_traceback(self, mocked_print) -> None:
        def failing_action() -> None:
            raise ValueError("örnek veri hatası")

        success = execute_safely(failing_action)

        self.assertFalse(success)
        mocked_print.assert_called_once()
        self.assertIn("örnek veri hatası", mocked_print.call_args.args[0])


if __name__ == "__main__":
    unittest.main()
