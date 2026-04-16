from __future__ import annotations
from datetime import datetime
from src.infrastructure.logging.log_formatter import append_json_log, append_yaml_log, append_md_log


def write_log(level: str, message: str, extra: dict | None = None):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "level": level.upper(),
        "message": message,
        **(extra or {}),
    }
    append_json_log(entry)
    append_yaml_log(entry)
    append_md_log(entry)
