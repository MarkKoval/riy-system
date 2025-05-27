"""
core — Основний модуль логіки ройової системи керування дронами.
"""

import logging
import os

from utils.config_loader import load_config

# Ініціалізація логування
logger = logging.getLogger("core")
logger.setLevel(logging.INFO)

log_format = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_format)
logger.addHandler(console_handler)

# Завантаження глобальної конфігурації при ініціалізації модуля
CONFIG_PATH = os.getenv("RIY_CONFIG_PATH", "config/system_config.yaml")

try:
    config = load_config(CONFIG_PATH)
    logger.info("Конфігурацію завантажено успішно.")
except Exception as e:
    config = None
    logger.error(f"Не вдалося завантажити конфігурацію: {e}")

# Імпорт основних класів пакету
from .swarm_manager import SwarmManager
from .drone_agent import DroneAgent
from .state_sync import StateSynchronizer

__all__ = ["SwarmManager", "DroneAgent", "StateSynchronizer", "config", "logger"]
