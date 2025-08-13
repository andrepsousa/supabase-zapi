import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

_LOGGER_CREATED = {}


def get_logger(name: str = "app") -> logging.Logger:
    if name in _LOGGER_CREATED:
        return _LOGGER_CREATED[name]

    level = os.getenv("LOG_LEVEL", "INFO").upper()
    log = logging.getLogger(name)
    log.setLevel(level)

    fmt = logging.Formatter(
        "[%(levelname)s] %(asctime)s %(name)s - %(message)s"
    )

    sh = logging.StreamHandler()
    sh.setFormatter(fmt)
    log.addHandler(sh)

    log_file = os.getenv("LOG_FILE")
    if log_file:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        fh = RotatingFileHandler(
            log_file, maxBytes=500_000, backupCount=3, encoding="utf-8"
        )
        fh.setFormatter(fmt)
        log.addHandler(fh)

    _LOGGER_CREATED[name] = log
    return log
