"""Tüm laboratuvar denetimlerini tek akışta çalıştırır."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

from modules.app_logging import configure_logging
from modules.config_tracking import run_simulated_config_tracking
from modules.discovery import discover_simulated_assets
from modules.local_socket_lab import run_local_socket_demo
from modules.notifier import format_alerts, notify_alerts
from modules.port_scan import assess_simulated_ports
from modules.storage import ensure_directory, load_json, save_json, timestamp


def build_summary(
    assets: list[dict],
    port_results: list[dict],
    config_alerts: list[str],
    local_socket_results: list[dict] | None = None,
) -> dict:
    """Denetim çıktılarını yönetici özeti için sayısallaştırır."""
    levels = Counter(
        finding["level"]
        for result in port_results
        for finding in result["findings"]
    )
    local_socket_results = local_socket_results or []
    return {
        "asset_count": len(assets),
        "open_port_count": sum(len(result["open_ports"]) for result in port_results),
        "high_risk_count": levels["high"],
        "medium_risk_count": levels["medium"],
        "info_count": levels["info"],
        "critical_config_change_count": len(config_alerts),
        "local_socket_open_count": sum(
            result["status"] == "open" for result in local_socket_results
        ),
    }


def save_text_summary(
    summary: dict,
    config_changes: list[str],
    alerts: list[str],
    notification: dict | None = None,
) -> Path:
    """Okunabilir metin raporu oluşturur."""
    report_path = ensure_directory("data/reports") / f"audit_summary_{timestamp()}.txt"
    lines = [
        "NETSECOPS LABORATUVAR DENETİM ÖZETİ",
        "=" * 39,
        "Çalışma modu: Simülasyon",
        f"Tespit edilen cihaz: {summary['asset_count']}",
        f"Toplam açık port: {summary['open_port_count']}",
        f"Yüksek riskli port bulgusu: {summary['high_risk_count']}",
        f"Orta riskli port bulgusu: {summary['medium_risk_count']}",
        f"Kritik config değişikliği: {summary['critical_config_change_count']}",
        f"Loopback üzerinde doğrulanan açık TCP portu: {summary['local_socket_open_count']}",
        "",
        "YAPILANDIRMA DEĞİŞİKLİKLERİ",
        *config_changes,
        "",
        "BİLDİRİM",
        format_alerts(alerts),
        f"Webhook durumu: {(notification or {}).get('status', 'not_run')}",
    ]
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report_path


def run_full_audit() -> dict:
    """Bütün simüle edilmiş denetimleri çalıştırır ve birleşik rapor üretir."""
    logger = configure_logging()
    logger.info("Tam laboratuvar denetimi başlatıldı.")

    settings = load_json("config/settings.json")
    assets, inventory_report = discover_simulated_assets()
    port_results, port_report = assess_simulated_ports()
    local_socket_results, local_socket_report = run_local_socket_demo()
    config_tracking = run_simulated_config_tracking()
    config_changes = config_tracking["changes"]
    alerts = config_tracking["alerts"]
    diff_report = config_tracking["report"]
    summary = build_summary(assets, port_results, alerts, local_socket_results)
    notification = notify_alerts(alerts, settings)
    if notification["status"] in {"failed", "rejected"}:
        logger.warning("Webhook bildirimi tamamlanamadı: %s", notification["error"])

    json_report = f"data/reports/audit_summary_{timestamp()}.json"
    save_json(
        json_report,
        {
            "mode": "simulation",
            "summary": summary,
            "artifacts": {
                "inventory": inventory_report,
                "port_report": port_report,
                "local_socket_report": local_socket_report,
                "config_diff": diff_report,
                "previous_config_backup": config_tracking["previous_backup"].name,
                "current_config_backup": config_tracking["current_backup"].name,
                "config_backup_integrity_verified": config_tracking["integrity_verified"],
            },
            "alerts": alerts,
            "notification": {
                "status": notification["status"],
                "webhook_attempted": notification["webhook_attempted"],
                "error": notification["error"],
            },
        },
    )
    text_report = save_text_summary(summary, config_changes, alerts, notification)
    logger.info("Tam denetim tamamlandı. Kritik değişiklik: %s", len(alerts))
    return {
        "summary": summary,
        "json_report": json_report,
        "text_report": str(text_report),
        "notification": notification,
    }
