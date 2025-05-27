"""
failsafe.py — Виявлення втрат зв’язку та реагування на збої в рої.
"""

import time
from threading import Lock
from utils.logger import get_logger

logger = get_logger("core.failsafe")


class FailsafeMonitor:
    """
    Відстежує останні пакети зв’язку від дронів та виявляє відмови.
    """

    def __init__(self, timeout_ms=1000):
        self.timeout = timeout_ms / 1000.0
        self.last_seen = {}  # drone_id -> timestamp
        self.lock = Lock()

    def update_heartbeat(self, drone_id: int):
        """
        Оновлює час останнього зв’язку з дроном.
        """
        with self.lock:
            self.last_seen[drone_id] = time.time()
            logger.debug(f"[Failsafe] Heartbeat від {drone_id}")

    def get_unresponsive_drones(self) -> list[int]:
        """
        Повертає список дронів, з якими втрачено зв’язок.
        """
        now = time.time()
        with self.lock:
            return [
                drone_id
                for drone_id, t in self.last_seen.items()
                if now - t > self.timeout
            ]

    def log_status(self):
        """
        Логування статусу всіх дронів.
        """
        offline = self.get_unresponsive_drones()
        if offline:
            logger.warning(f"[Failsafe] Втрачено зв’язок з: {offline}")
        else:
            logger.info("[Failsafe] Усі дрони активні")
