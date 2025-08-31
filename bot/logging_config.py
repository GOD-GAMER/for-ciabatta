import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

DEFAULT_LEVEL = "INFO"

LEVEL_MAP = {
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
    "NOTSET": logging.NOTSET,
}

def setup_logging():
    level_name = os.getenv("LOG_LEVEL", DEFAULT_LEVEL).upper()
    level = LEVEL_MAP.get(level_name, logging.INFO)

    # Root logger
    logger = logging.getLogger()
    logger.setLevel(level)

    # Ensure logs directory
    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s %(name)s: %(message)s", datefmt="%H:%M:%S"))

    # Rotating file handler
    fh = RotatingFileHandler(log_dir / "bakebot.log", maxBytes=2_000_000, backupCount=5, encoding="utf-8")
    fh.setLevel(level)
    fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(filename)s:%(lineno)d | %(message)s"))

    # Attach once
    if not any(isinstance(h, RotatingFileHandler) for h in logger.handlers):
        logger.addHandler(fh)
    if not any(isinstance(h, logging.StreamHandler) and not isinstance(h, RotatingFileHandler) for h in logger.handlers):
        logger.addHandler(ch)

    logging.getLogger("aiohttp.access").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)

    logging.getLogger(__name__).debug("Logging configured at level %s", level_name)

    return logger
