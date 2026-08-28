"""Uygulama günlükleme ayarları."""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler

from modules.storage import ensure_directory


def configure_logging() -> logging.Logger:
    """Konsol ve dönen dosya günlüğünü bir kez yapılandırır."""
    logger = logging.getLogger("netsecops")
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    log_path = ensure_directory("logs") / "app.log"
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler = RotatingFileHandler(
        log_path, maxBytes=500_000, backupCount=3, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger
