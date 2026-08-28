"""Simüle edilmiş ağ cihazı yapılandırma yedekleri."""

from __future__ import annotations

from pathlib import Path

from modules.storage import PROJECT_ROOT, ensure_directory, timestamp


SAMPLE_CONFIGS = {
    "baseline": """hostname lab-switch-01\n!\ninterface GigabitEthernet0/1\n switchport mode access\n switchport access vlan 10\n!\nip access-list extended MANAGEMENT_ONLY\n permit tcp 192.168.56.0 0.0.0.255 any eq 22\n deny ip any any log\n!\nend\n""",
    "changed": """hostname lab-switch-01\n!\ninterface GigabitEthernet0/1\n switchport mode access\n switchport access vlan 20\n!\nip access-list extended MANAGEMENT_ONLY\n permit tcp 192.168.56.0 0.0.0.255 any eq 22\n permit ip any any\n!\nend\n""",
}


def create_simulated_backup(version: str) -> Path:
    """İki kontrollü örnek yapılandırma sürümünden birini yedekler."""
    if version not in SAMPLE_CONFIGS:
        raise ValueError("Geçersiz yapılandırma sürümü.")

    directory = ensure_directory("data/backups/lab-switch-01")
    path = directory / f"{timestamp()}_{version}.txt"
    path.write_text(SAMPLE_CONFIGS[version], encoding="utf-8")
    return path


def list_backups() -> list[Path]:
    """Cihaza ait mevcut örnek yedekleri listeler."""
    directory = PROJECT_ROOT / "data/backups/lab-switch-01"
    return sorted(directory.glob("*.txt")) if directory.exists() else []
