from __future__ import annotations

import logging
from app.utils.paths import get_log_path


def setup_logging() -> None:
    logging.basicConfig(
        filename=get_log_path(),
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        encoding="utf-8",
    )
