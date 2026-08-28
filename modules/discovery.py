"""Simüle edilmiş ağ varlık keşfi işlemleri."""

from __future__ import annotations

from modules.storage import load_json, save_json, timestamp
from modules.validation import validate_assets, validate_settings


def discover_simulated_assets() -> tuple[list[dict], str]:
    """Laboratuvar envanterindeki aktif cihazları okur ve kayıt altına alır."""
    settings = load_json("config/settings.json")
    assets = load_json("config/simulated_network.json")
    allowed_network = validate_settings(settings)
    validate_assets(assets, allowed_network)
    output_path = f"data/inventory/inventory_{timestamp()}.json"
    save_json(output_path, {"mode": "simulation", "assets": assets})
    return assets, output_path
