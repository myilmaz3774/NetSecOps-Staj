import tempfile
import unittest
from pathlib import Path

from modules.config_backup import (
    metadata_path_for,
    save_backup,
    select_latest_backup_pair,
    validate_device_name,
    verify_backup_integrity,
)


class ConfigBackupTests(unittest.TestCase):
    def test_saves_config_with_version_suffix(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            backup = save_backup("hostname lab-switch\n", "baseline", Path(directory))

            self.assertTrue(backup.name.endswith("_baseline.txt"))
            self.assertEqual(backup.read_text(encoding="utf-8"), "hostname lab-switch\n")
            self.assertTrue(metadata_path_for(backup).exists())
            self.assertTrue(verify_backup_integrity(backup))

    def test_rejects_empty_config(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "Boş yapılandırma"):
                save_backup("   ", "baseline", Path(directory))

    def test_detects_modified_backup(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            backup = save_backup("hostname lab-switch\n", "baseline", Path(directory))
            backup.write_text("hostname modified\n", encoding="utf-8")

            self.assertFalse(verify_backup_integrity(backup))

    def test_selects_latest_verified_pair(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output_directory = Path(directory)
            first = save_backup("hostname baseline\n", "baseline", output_directory)
            second = save_backup("hostname changed\n", "changed", output_directory)

            previous, current = select_latest_backup_pair(output_directory)

            self.assertEqual((previous, current), (first, second))

    def test_requires_two_backups_for_comparison(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output_directory = Path(directory)
            save_backup("hostname baseline\n", "baseline", output_directory)

            with self.assertRaisesRegex(ValueError, "en az iki"):
                select_latest_backup_pair(output_directory)

    def test_rejects_unsafe_device_name(self) -> None:
        with self.assertRaisesRegex(ValueError, "Cihaz adı"):
            validate_device_name("../outside")


if __name__ == "__main__":
    unittest.main()
