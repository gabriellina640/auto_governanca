from __future__ import annotations

import os
from pathlib import Path

APP_DIR_NAME = "CadastroExcel"


def get_app_data_dir() -> Path:
    """Return a writable per-user app data folder."""
    base = os.getenv("APPDATA")
    if base:
        root = Path(base)
    else:
        root = Path.home() / ".config"
    path = root / APP_DIR_NAME
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_config_path() -> Path:
    return get_app_data_dir() / "config.json"


def get_log_path() -> Path:
    return get_app_data_dir() / "app.log"
