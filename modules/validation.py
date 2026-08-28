"""Laboratuvar ayarları ve örnek veriler için doğrulama kuralları."""

from __future__ import annotations

import ipaddress
import re
from typing import Any


MAC_PATTERN = re.compile(r"^(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$")


def _validate_ports(ports: Any, field_name: str) -> list[int]:
    if not isinstance(ports, list) or not ports:
        raise ValueError(f"{field_name} boş olmayan bir liste olmalıdır.")
    if any(not isinstance(port, int) or isinstance(port, bool) or not 1 <= port <= 65535 for port in ports):
        raise ValueError(f"{field_name} yalnızca 1-65535 arası portlar içermelidir.")
    if len(ports) != len(set(ports)):
        raise ValueError(f"{field_name} tekrarlanan port içeremez.")
    return ports


def validate_settings(settings: Any) -> ipaddress.IPv4Network | ipaddress.IPv6Network:
    """Ayar dosyasını doğrular ve izinli ağı döndürür."""
    if not isinstance(settings, dict):
        raise ValueError("Ayar dosyası JSON nesnesi olmalıdır.")
    if not isinstance(settings.get("project_name"), str) or not settings["project_name"].strip():
        raise ValueError("project_name boş olmayan bir metin olmalıdır.")
    try:
        network = ipaddress.ip_network(settings.get("allowed_network"), strict=True)
    except (TypeError, ValueError) as error:
        raise ValueError("allowed_network geçerli bir CIDR olmalıdır.") from error

    monitored_ports = _validate_ports(settings.get("ports"), "ports")
    high_risk_ports = _validate_ports(settings.get("high_risk_ports"), "high_risk_ports")
    if not set(high_risk_ports).issubset(monitored_ports):
        raise ValueError("high_risk_ports, izlenen ports listesinin alt kümesi olmalıdır.")
    return network


def validate_assets(assets: Any, allowed_network: Any) -> None:
    """Simüle cihaz kayıtlarını ve izinli CIDR sınırını doğrular."""
    if not isinstance(assets, list) or not assets:
        raise ValueError("Simüle cihaz listesi boş olmayan bir liste olmalıdır.")

    seen_ips: set[str] = set()
    seen_macs: set[str] = set()
    seen_hostnames: set[str] = set()
    for index, asset in enumerate(assets, start=1):
        if not isinstance(asset, dict):
            raise ValueError(f"{index}. cihaz kaydı JSON nesnesi olmalıdır.")
        hostname = asset.get("hostname")
        ip_value = asset.get("ip")
        mac = asset.get("mac")
        if not isinstance(hostname, str) or not hostname.strip():
            raise ValueError(f"{index}. cihazın hostname alanı geçersiz.")
        try:
            address = ipaddress.ip_address(ip_value)
        except (TypeError, ValueError) as error:
            raise ValueError(f"{hostname} için IP adresi geçersiz.") from error
        if address not in allowed_network:
            raise ValueError(f"{hostname} izinli laboratuvar CIDR kapsamı dışında.")
        if not isinstance(mac, str) or not MAC_PATTERN.fullmatch(mac):
            raise ValueError(f"{hostname} için MAC adresi geçersiz.")
        _validate_ports(asset.get("open_ports"), f"{hostname}.open_ports")

        normalized_mac = mac.lower()
        if str(address) in seen_ips or normalized_mac in seen_macs or hostname in seen_hostnames:
            raise ValueError("Simüle cihaz kayıtlarında tekrarlanan IP, MAC veya hostname var.")
        seen_ips.add(str(address))
        seen_macs.add(normalized_mac)
        seen_hostnames.add(hostname)
