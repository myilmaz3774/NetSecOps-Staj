"""Yapılandırma değişikliklerinin satır bazlı analizi."""

from __future__ import annotations

import difflib
from pathlib import Path

from modules.storage import save_json, timestamp


CRITICAL_TERMS = ("permit ip any any", "transport input telnet", "no ip access-list")


def compare_configs(old_path: Path, new_path: Path) -> tuple[list[str], list[str], str]:
    """İki yapılandırma yedeğini karşılaştırır ve kritik satırları işaretler."""
    old_lines = old_path.read_text(encoding="utf-8").splitlines()
    new_lines = new_path.read_text(encoding="utf-8").splitlines()
    diff = list(
        difflib.unified_diff(
            old_lines, new_lines, fromfile=old_path.name, tofile=new_path.name, lineterm=""
        )
    )
    changes = [line for line in diff if line.startswith(("+", "-")) and not line.startswith(("+++", "---"))]
    alerts = [line for line in changes if any(term in line.lower() for term in CRITICAL_TERMS)]
    output_path = f"data/reports/config_diff_{timestamp()}.json"
    save_json(
        output_path,
        {"old_backup": old_path.name, "new_backup": new_path.name, "changes": changes, "alerts": alerts},
    )
    return changes, alerts, output_path
