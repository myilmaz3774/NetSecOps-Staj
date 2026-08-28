"""Simüle config yedekleme ve değişiklik takip iş akışı."""

from __future__ import annotations

from modules.config_backup import create_simulated_backup, latest_backup_pair
from modules.diff_check import compare_configs


def run_simulated_config_tracking(device_name: str = "lab-switch-01") -> dict:
    """İki config sürümünü yedekler ve geçmişteki son iki yedeği karşılaştırır."""
    create_simulated_backup("baseline", device_name)
    create_simulated_backup("changed", device_name)
    previous, current = latest_backup_pair(device_name)
    changes, alerts, report = compare_configs(previous, current)
    return {
        "device_name": device_name,
        "previous_backup": previous,
        "current_backup": current,
        "integrity_verified": True,
        "changes": changes,
        "alerts": alerts,
        "report": report,
    }
