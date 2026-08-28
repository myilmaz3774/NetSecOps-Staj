"""Dosya ve klasör işlemleri için yardımcı fonksiyonlar."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def load_json(relative_path: str) -> Any:
    """Proje içindeki bir JSON dosyasını okur."""
    with (PROJECT_ROOT / relative_path).open("r", encoding="utf-8") as file:
        return json.load(file)


def timestamp() -> str:
    """Dosya isimlerinde kullanılacak zaman damgasını üretir."""
    return datetime.now().strftime("%Y%m%d_%H%M%S_%f")


def ensure_directory(relative_path: str) -> Path:
    """Gerekli çıktı klasörünü oluşturur ve yolunu döndürür."""
    directory = PROJECT_ROOT / relative_path
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def save_json(relative_path: str, content: Any) -> Path:
    """Veriyi UTF-8 JSON biçiminde kaydeder."""
    target = PROJECT_ROOT / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8") as file:
        json.dump(content, file, ensure_ascii=False, indent=2)
    return target
