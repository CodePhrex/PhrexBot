"""Persist only explicitly approved operational event messages."""
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import os

EVENTS = frozenset({
    "command denied", "authorized command received",
    "natural intelligence unavailable", "Discovery notification unavailable",
    "Application runtime starting", "Application runtime stopped",
    "Application runtime failed",
})

class EventFilter(logging.Filter):
    def filter(self, record):
        return isinstance(record.msg, str) and record.msg in EVENTS and not record.args and not record.exc_info and not record.stack_info

def configure():
    if os.name != "nt":
        return
    folder = Path(os.environ["LOCALAPPDATA"]) / "CodePhrex" / "Phrex" / "logs"
    folder.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("phrex.audit")
    logger.setLevel(logging.INFO)
    if any(getattr(h, "_phrex_events", False) for h in logger.handlers):
        return
    handler = RotatingFileHandler(folder / "application.log", maxBytes=1048576, backupCount=3, encoding="utf-8")
    handler._phrex_events = True
    handler.addFilter(EventFilter())
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(handler)
