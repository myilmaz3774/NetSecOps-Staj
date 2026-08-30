"""Kritik bulgular için yerel ve isteğe bağlı webhook bildirimi."""

from __future__ import annotations

import json
import os
from collections.abc import Iterable
from urllib import error, parse, request


def format_alerts(alerts: Iterable[str]) -> str:
    """Kritik bulguları güvenli, yerel bir bildirim metnine dönüştürür."""
    alert_list = list(alerts)
    if not alert_list:
        return "Kritik değişiklik tespit edilmedi."
    lines = ["KRİTİK YAPILANDIRMA DEĞİŞİKLİĞİ"]
    lines.extend(f"- {alert}" for alert in alert_list)
    return "\n".join(lines)


def validate_webhook_url(url: str) -> None:
    """Webhook URL'sini HTTPS veya yerel HTTP ile sınırlar."""
    parsed = parse.urlparse(url)
    is_local_http = parsed.scheme == "http" and parsed.hostname in {"127.0.0.1", "localhost", "::1"}
    if parsed.scheme != "https" and not is_local_http:
        raise ValueError("Webhook yalnızca HTTPS veya loopback HTTP kullanabilir.")
    if not parsed.netloc:
        raise ValueError("Webhook URL'si geçerli bir hedef içermelidir.")


def send_webhook(alerts: Iterable[str], url: str, timeout: float = 3) -> dict:
    """Kritik bulguları JSON payload olarak webhook'a iletir."""
    alert_list = list(alerts)
    if not alert_list:
        return {"status": "no_alerts", "webhook_attempted": False, "error": None}
    validate_webhook_url(url)
    payload = json.dumps(
        {
            "source": "netsecops-lab",
            "alert_count": len(alert_list),
            "message": format_alerts(alert_list),
        },
        ensure_ascii=False,
    ).encode("utf-8")
    request_object = request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with request.urlopen(request_object, timeout=timeout) as response:
            status_code = getattr(response, "status", 200)
        if not 200 <= status_code < 300:
            return {"status": "failed", "webhook_attempted": True, "error": f"HTTP {status_code}"}
    except (error.URLError, TimeoutError, OSError) as request_error:
        return {"status": "failed", "webhook_attempted": True, "error": str(request_error)}
    return {"status": "sent", "webhook_attempted": True, "error": None}


def notify_alerts(alerts: Iterable[str], settings: dict) -> dict:
    """Ayarları okuyarak bildirimi kapalı, eksik veya etkin olarak yönetir."""
    alert_list = list(alerts)
    message = format_alerts(alert_list)
    notification_settings = settings.get("notifications", {})
    if not alert_list:
        return {"status": "no_alerts", "webhook_attempted": False, "error": None, "message": message}
    if not notification_settings.get("enabled", False):
        return {"status": "disabled", "webhook_attempted": False, "error": None, "message": message}

    env_name = notification_settings.get("webhook_url_env", "NETSECOPS_WEBHOOK_URL")
    url = os.getenv(env_name)
    if not url:
        return {"status": "not_configured", "webhook_attempted": False, "error": "Webhook ortam değişkeni ayarlı değil.", "message": message}
    try:
        result = send_webhook(alert_list, url, notification_settings.get("timeout_seconds", 3))
    except ValueError as validation_error:
        result = {"status": "rejected", "webhook_attempted": False, "error": str(validation_error)}
    result["message"] = message
    return result
