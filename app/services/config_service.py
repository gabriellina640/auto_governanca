from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from app.utils.paths import get_config_path

DEFAULT_CONFIG: dict[str, Any] = {
    "app_name": "Cadastro Inteligente Excel",
    "excel_path": "",
    "sheet_name": "Banco de dados",
    "form_fields": [
        "Data",
        "Normativa",
        "Nome",
        "Evento",
        "Detalhamento do Evento",
        "Função",
        "Temática",
        "Perenidade",
    ],
    "auto_columns": {
        "id": "ID",
        "timestamp": "TimestampInclusao",
        "user": "UsuarioInclusao",
    },
    "hidden_form_fields": ["ID", "TimestampInclusao", "UsuarioInclusao"],
    "required_fields": [],
    "date_fields": ["Data"],
    "display_date_format": "%d/%m/%Y",
    "excel_date_format": "DD/MM/YYYY",
    "backup_enabled": True,
    "backup_folder": "backups",
}


class ConfigService:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or get_config_path()
        self.config = self.load()

    def load(self) -> dict[str, Any]:
        if not self.path.exists():
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text(json.dumps(DEFAULT_CONFIG, indent=2, ensure_ascii=False), encoding="utf-8")
            return deepcopy(DEFAULT_CONFIG)

        try:
            loaded = json.loads(self.path.read_text(encoding="utf-8"))
        except Exception:
            loaded = {}

        merged = deepcopy(DEFAULT_CONFIG)
        merged.update(loaded)
        merged["auto_columns"] = {**DEFAULT_CONFIG["auto_columns"], **loaded.get("auto_columns", {})}
        return merged

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.config, indent=2, ensure_ascii=False), encoding="utf-8")

    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self.config[key] = value
        self.save()
