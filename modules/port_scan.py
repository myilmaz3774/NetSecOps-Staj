"""Simüle edilmiş port ve risk denetimi işlemleri."""

from __future__ import annotations

from modules.storage import load_json, save_json, timestamp


RISK_LABELS = {
    21: "Yüksek - FTP açık",
    23: "Yüksek - Telnet açık",
    80: "Orta - Şifrelenmemiş HTTP açık",
    445: "Yüksek - SMB açık",
    3389: "Orta - RDP açık"
}


def assess_simulated_ports() -> tuple[list[dict], str]:
    """Örnek envanterdeki tanımlı kritik portları değerlendirir."""
    settings = load_json("config/settings.json")
    assets = load_json("config/simulated_network.json")
    monitored_ports = set(settings["ports"])
    results = []

    for asset in assets:
        open_ports = [port for port in asset["open_ports"] if port in monitored_ports]
        findings = [
            {"port": port, "risk": RISK_LABELS.get(port, "Bilgilendirici - Açık port")}
            for port in open_ports
        ]
        results.append(
            {
                "ip": asset["ip"],
                "hostname": asset["hostname"],
                "open_ports": open_ports,
                "findings": findings,
            }
        )

    output_path = f"data/reports/port_report_{timestamp()}.json"
    save_json(output_path, {"mode": "simulation", "results": results})
    return results, output_path
