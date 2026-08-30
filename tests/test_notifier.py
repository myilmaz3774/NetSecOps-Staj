import json
import unittest
from unittest.mock import patch

from modules.notifier import notify_alerts, validate_webhook_url


class _FakeResponse:
    status = 204

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return None


class NotifierTests(unittest.TestCase):
    def test_disabled_webhook_does_not_send(self) -> None:
        settings = {"notifications": {"enabled": False}}

        with patch("modules.notifier.request.urlopen") as mocked_urlopen:
            result = notify_alerts(["+ permit ip any any"], settings)

        self.assertEqual(result["status"], "disabled")
        mocked_urlopen.assert_not_called()

    def test_missing_enabled_webhook_is_not_configured(self) -> None:
        settings = {
            "notifications": {"enabled": True, "webhook_url_env": "NETSECOPS_TEST_MISSING"}
        }

        with patch.dict("os.environ", {}, clear=True):
            result = notify_alerts(["+ permit ip any any"], settings)

        self.assertEqual(result["status"], "not_configured")

    @patch("modules.notifier.request.urlopen", return_value=_FakeResponse())
    @patch.dict("os.environ", {"NETSECOPS_TEST_WEBHOOK": "https://example.invalid/hook"}, clear=True)
    def test_sends_https_webhook_without_exposing_credentials(self, mocked_urlopen) -> None:
        settings = {
            "notifications": {
                "enabled": True,
                "webhook_url_env": "NETSECOPS_TEST_WEBHOOK",
                "timeout_seconds": 3,
            }
        }

        result = notify_alerts(["+ permit ip any any"], settings)

        self.assertEqual(result["status"], "sent")
        request_object = mocked_urlopen.call_args.args[0]
        payload = json.loads(request_object.data.decode("utf-8"))
        self.assertEqual(payload["source"], "netsecops-lab")
        self.assertNotIn("password", payload)

    def test_rejects_non_loopback_http_webhook(self) -> None:
        with self.assertRaisesRegex(ValueError, "HTTPS veya loopback"):
            validate_webhook_url("http://example.com/hook")


if __name__ == "__main__":
    unittest.main()
