import logging
import os
from src.utils.logger import get_logger


def test_logger_level_from_env(monkeypatch, tmp_path):
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("LOG_FILE", str(tmp_path / "app.log"))
    log = get_logger("test-logger")
    assert log.level == logging.DEBUG
    before = len(log.handlers)
    again = get_logger("test-logger")
    assert len(again.handlers) == before
