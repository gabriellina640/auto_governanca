from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from app.services.config_service import ConfigService
from app.services.log_service import setup_logging
from app.ui.main_window import MainWindow


def load_stylesheet(app: QApplication) -> None:
    qss_path = Path(__file__).parent / "app" / "ui" / "styles.qss"
    if qss_path.exists():
        app.setStyleSheet(qss_path.read_text(encoding="utf-8"))


def main() -> int:
    setup_logging()
    app = QApplication(sys.argv)
    app.setApplicationName("Cadastro Inteligente Excel")
    load_stylesheet(app)

    config_service = ConfigService()
    window = MainWindow(config_service)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
