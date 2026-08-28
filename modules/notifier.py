"""Kritik bulgular için yerel bildirim üretimi."""

from __future__ import annotations

from collections.abc import Iterable


def format_alerts(alerts: Iterable[str]) -> str:
    """Kritik bulguları güvenli, yerel bir bildirim metnine dönüştürür."""
    alert_list = list(alerts)
    if not alert_list:
        return "Kritik değişiklik tespit edilmedi."
    lines = ["KRİTİK YAPILANDIRMA DEĞİŞİKLİĞİ"]
    lines.extend(f"- {alert}" for alert in alert_list)
    return "\n".join(lines)
