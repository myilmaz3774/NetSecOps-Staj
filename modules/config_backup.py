"""Simüle edilmiş ağ cihazı yapılandırma yedekleri."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from modules.storage import PROJECT_ROOT, ensure_directory, timestamp


SAMPLE_CONFIG_DIR = PROJECT_ROOT / "fixtures/configs"
DEVICE_NAME_PATTERN = re.compile(r"^[A-Za-z0-9._-]+$")
VALID_VERSIONS = {"baseline", "changed"}


def validate_device_name(device_name: str) -> str:
    """Cihaz adının güvenli bir klasör adı olarak kullanılabildiğini doğrular."""
    if not isinstance(device_name, str) or not DEVICE_NAME_PATTERN.fullmatch(device_name):
        raise ValueError("Cihaz adı yalnızca harf, sayı, nokta, tire ve alt çizgi içerebilir.")
    return device_name


def metadata_path_for(config_path: Path) -> Path:
    """Bir config yedeğine ait metadata dosyasının yolunu döndürür."""
    return config_path.with_suffix(".metadata.json")


def save_backup(
    content: str,
    version: str,
    output_directory: Path,
    device_name: str = "lab-switch-01",
) -> Path:
    """Config ve SHA-256 bütünlük bilgisini zaman damgalı olarak kaydeder."""
    if not content.strip():
        raise ValueError("Boş yapılandırma yedeklenemez.")
    if version not in VALID_VERSIONS:
        raise ValueError("Geçersiz yapılandırma sürümü.")
    validate_device_name(device_name)

    output_directory.mkdir(parents=True, exist_ok=True)
    backup_timestamp = timestamp()
    path = output_directory / f"{backup_timestamp}_{version}.txt"
    content_bytes = content.encode("utf-8")
    path.write_bytes(content_bytes)
    metadata = {
        "device_name": device_name,
        "version": version,
        "created_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "file_name": path.name,
        "size_bytes": len(content_bytes),
        "sha256": hashlib.sha256(content_bytes).hexdigest(),
        "source": "simulation",
    }
    metadata_path_for(path).write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return path


def create_simulated_backup(version: str, device_name: str = "lab-switch-01") -> Path:
    """İki kontrollü örnek yapılandırma sürümünden birini yedekler."""
    if version not in VALID_VERSIONS:
        raise ValueError("Geçersiz yapılandırma sürümü.")
    validate_device_name(device_name)

    source = SAMPLE_CONFIG_DIR / f"{version}.txt"
    content = source.read_text(encoding="utf-8")
    directory = ensure_directory(f"data/backups/{device_name}")
    return save_backup(content, version, directory, device_name)


def list_backups(device_name: str = "lab-switch-01") -> list[Path]:
    """Cihaza ait mevcut örnek yedekleri listeler."""
    validate_device_name(device_name)
    directory = PROJECT_ROOT / "data/backups" / device_name
    return sorted(directory.glob("*.txt")) if directory.exists() else []


def load_backup_metadata(config_path: Path) -> dict[str, Any]:
    """Yedeğe ait metadata kaydını okuyup temel alanlarını doğrular."""
    metadata_path = metadata_path_for(config_path)
    try:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise ValueError(f"Metadata dosyası bulunamadı: {metadata_path.name}") from error
    except json.JSONDecodeError as error:
        raise ValueError(f"Metadata dosyası geçerli JSON değil: {metadata_path.name}") from error

    required_fields = {
        "device_name",
        "version",
        "created_at",
        "file_name",
        "size_bytes",
        "sha256",
        "source",
    }
    if not isinstance(metadata, dict) or not required_fields.issubset(metadata):
        raise ValueError(f"Metadata alanları eksik: {metadata_path.name}")
    return metadata


def verify_backup_integrity(config_path: Path) -> bool:
    """Config içeriğinin metadata SHA-256 ve boyut bilgisiyle eşleştiğini doğrular."""
    metadata = load_backup_metadata(config_path)
    content_bytes = config_path.read_bytes()
    return (
        metadata["file_name"] == config_path.name
        and metadata["size_bytes"] == len(content_bytes)
        and metadata["sha256"] == hashlib.sha256(content_bytes).hexdigest()
    )


def select_latest_backup_pair(directory: Path) -> tuple[Path, Path]:
    """Klasördeki son iki doğrulanmış config yedeğini seçer."""
    backups = sorted(directory.glob("*.txt")) if directory.exists() else []
    if len(backups) < 2:
        raise ValueError("Karşılaştırma için en az iki config yedeği gereklidir.")

    previous, current = backups[-2:]
    for backup in (previous, current):
        if not verify_backup_integrity(backup):
            raise ValueError(f"Config yedeği bütünlük kontrolünü geçemedi: {backup.name}")
    return previous, current


def latest_backup_pair(device_name: str = "lab-switch-01") -> tuple[Path, Path]:
    """Belirtilen cihazın son iki doğrulanmış yedeğini döndürür."""
    validate_device_name(device_name)
    return select_latest_backup_pair(PROJECT_ROOT / "data/backups" / device_name)
