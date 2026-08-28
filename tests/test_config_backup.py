import tempfile
import unittest
from pathlib import Path

from modules.config_backup import save_backup


class ConfigBackupTests(unittest.TestCase):
    def test_saves_config_with_version_suffix(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            backup = save_backup("hostname lab-switch\n", "baseline", Path(directory))

            self.assertTrue(backup.name.endswith("_baseline.txt"))
            self.assertEqual(backup.read_text(encoding="utf-8"), "hostname lab-switch\n")

    def test_rejects_empty_config(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "Boş yapılandırma"):
                save_backup("   ", "baseline", Path(directory))


if __name__ == "__main__":
    unittest.main()
