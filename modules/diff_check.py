"""Yapılandırma değişikliklerinin satır bazlı analizi."""

from __future__ import annotations

import difflib
import hashlib
from pathlib import Path

from modules.storage import save_json, timestamp


CRITICAL_ADDED_TERMS = ("permit ip any any", "transport input telnet", "no ip access-list")
CRITICAL_REMOVED_TERMS = ("deny ip any any", "transport input ssh")


def analyze_config_lines(old_lines: list[str], new_lines: list[str]) -> tuple[list[str], list[str]]:
    """Yapılandırma satırlarını karşılaştırır ve kritik değişiklikleri ayırır."""
    diff = list(
        difflib.unified_diff(old_lines, new_lines, fromfile="previous", tofile="current", lineterm="")
    )
    changes = [
        line
        for line in diff
        if line.startswith(("+", "-")) and not line.startswith(("+++", "---"))
    ]
    alerts = []
    for line in changes:
        normalized = line[1:].strip().lower()
        if line.startswith("+") and any(term in normalized for term in CRITICAL_ADDED_TERMS):
            alerts.append(line)
        if line.startswith("-") and any(term in normalized for term in CRITICAL_REMOVED_TERMS):
            alerts.append(line)
    return changes, alerts


def compare_configs(old_path: Path, new_path: Path) -> tuple[list[str], list[str], str]:
    """İki yapılandırma yedeğini karşılaştırır ve kritik satırları işaretler."""
    old_lines = old_path.read_text(encoding="utf-8").splitlines()
    new_lines = new_path.read_text(encoding="utf-8").splitlines()
    changes, alerts = analyze_config_lines(old_lines, new_lines)
    output_path = f"data/reports/config_diff_{timestamp()}.json"
    save_json(
        output_path,
        {
            "old_backup": old_path.name,
            "new_backup": new_path.name,
            "old_sha256": hashlib.sha256(old_path.read_bytes()).hexdigest(),
            "new_sha256": hashlib.sha256(new_path.read_bytes()).hexdigest(),
            "changes": changes,
            "alerts": alerts,
        },
    )
    return changes, alerts, output_path
