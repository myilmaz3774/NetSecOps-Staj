"""Simüle edilmiş ağ cihazı yapılandırma yedekleri."""

from __future__ import annotations

from pathlib import Path

from modules.storage import PROJECT_ROOT, ensure_directory, timestamp


SAMPLE_CONFIG_DIR = PROJECT_ROOT / "fixtures/configs"


def save_backup(content: str, version: str, output_directory: Path) -> Path:
    """Verilen yapılandırmayı zaman damgalı bir yedek dosyasına kaydeder."""
    if not content.strip():
        raise ValueError("Boş yapılandırma yedeklenemez.")
    if version not in {"baseline", "changed"}:
        raise ValueError("Geçersiz yapılandırma sürümü.")
    output_directory.mkdir(parents=True, exist_ok=True)
    path = output_directory / f"{timestamp()}_{version}.txt"
    path.write_text(content, encoding="utf-8")
    return path


def create_simulated_backup(version: str) -> Path:
    """İki kontrollü örnek yapılandırma sürümünden birini yedekler."""
    if version not in {"baseline", "changed"}:
        raise ValueError("Geçersiz yapılandırma sürümü.")

    source = SAMPLE_CONFIG_DIR / f"{version}.txt"
    content = source.read_text(encoding="utf-8")
    directory = ensure_directory("data/backups/lab-switch-01")
    return save_backup(content, version, directory)


def list_backups() -> list[Path]:
    """Cihaza ait mevcut örnek yedekleri listeler."""
    directory = PROJECT_ROOT / "data/backups/lab-switch-01"
    return sorted(directory.glob("*.txt")) if directory.exists() else []
