"""Simüle edilmiş ağ varlık keşfi işlemleri."""

from __future__ import annotations

from modules.storage import load_json, save_json, timestamp


def discover_simulated_assets() -> tuple[list[dict], str]:
    """Laboratuvar envanterindeki aktif cihazları okur ve kayıt altına alır."""
    assets = load_json("config/simulated_network.json")
    output_path = f"data/inventory/inventory_{timestamp()}.json"
    save_json(output_path, {"mode": "simulation", "assets": assets})
    return assets, output_path
