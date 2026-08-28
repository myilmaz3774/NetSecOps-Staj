"""NetSecOps laboratuvar otomasyonunun komut satırı arayüzü."""

from modules.config_backup import create_simulated_backup
from modules.diff_check import compare_configs
from modules.discovery import discover_simulated_assets
from modules.port_scan import assess_simulated_ports


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
    baseline = create_simulated_backup("baseline")
    changed = create_simulated_backup("changed")
    changes, alerts, report = compare_configs(baseline, changed)
    print("\nYapılandırma farkları:")
    for line in changes:
        print(line)
    if alerts:
        print("\nKRİTİK UYARILAR:")
        for alert in alerts:
            print(f"- {alert}")
    print(f"Diff raporu kaydedildi: {report}")


def main() -> None:
    while True:
        print("\nNetSecOps Laboratory")
        print("1 - Simüle edilmiş varlık keşfi")
        print("2 - Simüle edilmiş port ve risk denetimi")
        print("3 - Simüle edilmiş config yedekleme ve diff")
        print("0 - Çıkış")
        choice = input("Seçiminiz: ").strip()
        if choice == "1":
            print_assets()
        elif choice == "2":
            print_port_report()
        elif choice == "3":
            create_and_compare_backups()
        elif choice == "0":
            print("Uygulama kapatıldı.")
            break
        else:
            print("Geçersiz seçim yaptınız.")


if __name__ == "__main__":
    main()
