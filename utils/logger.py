"""
logger.py — Уніфікована система логування для всіх модулів системи "Рій".
"""

import logging
import os
from logging.handlers import RotatingFileHandler

LOG_LEVEL = os.getenv("RIY_LOG_LEVEL", "INFO").upper()
LOG_FILE = os.getenv("RIY_LOG_FILE", "logs/swarm.log")
MAX_MB = int(os.getenv("RIY_LOG_MAX_MB", 5))
BACKUP_COUNT = int(os.getenv("RIY_LOG_BACKUP_COUNT", 3))


def get_logger(name: str) -> logging.Logger:
    """
    Повертає налаштований логер з іменем модуля.
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))

    if not logger.handlers:
        formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(name)s: %(message)s")

        # Консольний лог
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)

        # Файловий лог з обмеженням розміру
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        file_handler = RotatingFileHandler(
            LOG_FILE, maxBytes=MAX_MB * 1024 * 1024, backupCount=BACKUP_COUNT, encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
