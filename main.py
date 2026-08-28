"""NetSecOps laboratuvar otomasyonunun komut satırı arayüzü."""

import argparse
import json
import sys
from collections.abc import Callable

from modules.app_logging import configure_logging
from modules.config_tracking import run_simulated_config_tracking
from modules.discovery import discover_simulated_assets
from modules.local_socket_lab import run_local_socket_demo
from modules.port_scan import assess_simulated_ports
from modules.workflow import run_full_audit


def configure_console_encoding() -> None:
    """Windows terminallerinde Türkçe çıktının UTF-8 yazılmasını güvenceye alır."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8", errors="replace")


def execute_safely(action: Callable[[], None]) -> bool:
    """Beklenen kullanıcı ve dosya hatalarını anlaşılır biçimde raporlar."""
    try:
        action()
        return True
    except (FileNotFoundError, json.JSONDecodeError, ValueError, OSError) as error:
        logger = configure_logging()
        logger.error("İşlem tamamlanamadı: %s", error)
        print(f"\nHATA: İşlem tamamlanamadı: {error}")
        return False


def print_assets() -> None:
    assets, report = discover_simulated_assets()
    print("\nSimüle edilmiş aktif cihazlar:")
    for asset in assets:
        print(f"- {asset['hostname']}: {asset['ip']} | {asset['mac']}")
    print(f"Envanter kaydedildi: {report}")


def print_port_report() -> None:
    results, report = assess_simulated_ports()
    print("\nPort ve risk değerlendirmesi:")
    for result in results:
        print(f"- {result['hostname']} ({result['ip']}): {result['open_ports']}")
        for finding in result["findings"]:
            print(f"  * {finding['port']}: {finding['risk']}")
    print(f"Rapor kaydedildi: {report}")


def create_and_compare_backups() -> None:
    result = run_simulated_config_tracking()
    print("\nYapılandırma farkları:")
    print(f"Önceki yedek: {result['previous_backup'].name}")
    print(f"Güncel yedek: {result['current_backup'].name}")
    print("Bütünlük kontrolü: başarılı")
    for line in result["changes"]:
        print(line)
    if result["alerts"]:
        print("\nKRİTİK UYARILAR:")
        for alert in result["alerts"]:
            print(f"- {alert}")
    print(f"Diff raporu kaydedildi: {result['report']}")


def print_full_audit() -> None:
    result = run_full_audit()
    summary = result["summary"]
    print("\nTam laboratuvar denetimi tamamlandı:")
    print(f"- Cihaz sayısı: {summary['asset_count']}")
    print(f"- Açık port sayısı: {summary['open_port_count']}")
    print(f"- Yüksek riskli port bulgusu: {summary['high_risk_count']}")
    print(f"- Kritik config değişikliği: {summary['critical_config_change_count']}")
    print(f"- Loopback açık TCP portu: {summary['local_socket_open_count']}")
    print(f"- JSON raporu: {result['json_report']}")
    print(f"- Metin raporu: {result['text_report']}")


def print_local_socket_report() -> None:
    results, report = run_local_socket_demo()
    print("\nYerel TCP laboratuvar sonucu:")
    for result in results:
        print(f"- 127.0.0.1:{result['port']} -> {result['status']}")
    print(f"Rapor kaydedildi: {report}")


def main() -> None:
    configure_logging()
    while True:
        print("\nNetSecOps Laboratory")
        print("1 - Simüle edilmiş varlık keşfi")
        print("2 - Simüle edilmiş port ve risk denetimi")
        print("3 - Simüle edilmiş config yedekleme ve diff")
        print("4 - Tam laboratuvar denetimi")
        print("5 - Yerel TCP soket laboratuvarı")
        print("0 - Çıkış")
        choice = input("Seçiminiz: ").strip()
        if choice == "1":
            execute_safely(print_assets)
        elif choice == "2":
            execute_safely(print_port_report)
        elif choice == "3":
            execute_safely(create_and_compare_backups)
        elif choice == "4":
            execute_safely(print_full_audit)
        elif choice == "5":
            execute_safely(print_local_socket_report)
        elif choice == "0":
            print("Uygulama kapatıldı.")
            break
        else:
            print("Geçersiz seçim yaptınız.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="NetSecOps simülasyon laboratuvarı")
    parser.add_argument(
        "--run",
        choices=("menu", "discovery", "ports", "config", "local", "all"),
        default="menu",
        help="Çalıştırılacak laboratuvar işlemi",
    )
    return parser.parse_args()


if __name__ == "__main__":
    configure_console_encoding()
    args = parse_args()
    actions = {
        "menu": main,
        "discovery": print_assets,
        "ports": print_port_report,
        "config": create_and_compare_backups,
        "local": print_local_socket_report,
        "all": print_full_audit,
    }
    execute_safely(actions[args.run])
