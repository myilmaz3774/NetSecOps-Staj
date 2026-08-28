"""Simüle edilmiş port ve risk denetimi işlemleri."""

from __future__ import annotations

from modules.storage import load_json, save_json, timestamp


RISK_DETAILS = {
    21: ("high", "Yüksek - FTP açık"),
    23: ("high", "Yüksek - Telnet açık"),
    80: ("medium", "Orta - Şifrelenmemiş HTTP açık"),
    445: ("high", "Yüksek - SMB açık"),
    3389: ("medium", "Orta - RDP açık"),
}


def assess_assets(assets: list[dict], monitored_ports: set[int]) -> list[dict]:
    """Verilen cihaz listesindeki açık portları risk seviyelerine ayırır."""
    results = []

    for asset in assets:
        open_ports = [port for port in asset["open_ports"] if port in monitored_ports]
        findings = []
        for port in open_ports:
            level, description = RISK_DETAILS.get(
                port, ("info", "Bilgilendirici - Açık port")
            )
            findings.append({"port": port, "level": level, "risk": description})
        results.append(
            {
                "ip": asset["ip"],
                "hostname": asset["hostname"],
                "open_ports": open_ports,
                "findings": findings,
            }
        )

    return results


def assess_simulated_ports() -> tuple[list[dict], str]:
    """Örnek envanterdeki tanımlı kritik portları değerlendirir."""
    settings = load_json("config/settings.json")
    assets = load_json("config/simulated_network.json")
    monitored_ports = set(settings["ports"])
    results = assess_assets(assets, monitored_ports)

    output_path = f"data/reports/port_report_{timestamp()}.json"
    save_json(output_path, {"mode": "simulation", "results": results})
    return results, output_path
