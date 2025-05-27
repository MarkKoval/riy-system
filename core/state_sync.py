"""
state_sync.py — Модуль для синхронізації станів між дронами.
"""

import time
from threading import Lock

from utils.logger import get_logger

logger = get_logger("core.state_sync")


class StateSynchronizer:
    """
    Клас для зберігання та оновлення станів дронів у рої.
    """

    def __init__(self, self_id: int, timeout_ms: int = 2000):
        self.self_id = self_id
        self.timeout = timeout_ms / 1000.0
        self._lock = Lock()
        self._state_table = {}  # drone_id -> { "position": [...], "timestamp": ... }

    def update_state(self, drone_id: int, state: dict):
        """
        Оновлює стан дрона на основі вхідного повідомлення.
        """
        if drone_id == self.self_id:
            return  # Ігноруємо власний стан

        with self._lock:
            self._state_table[drone_id] = {
                "position": state.get("position", [0, 0, 0]),
                "status": state.get("status", "unknown"),
                "timestamp": time.time()
            }
            logger.debug(f"[Drone {self.self_id}] Оновлено стан дрона {drone_id}")

    def get_alive_drones(self) -> list[int]:
        """
        Повертає список дронів, які не втратили зв'язок (на основі timeout).
        """
        now = time.time()
        with self._lock:
            return [
                drone_id
                for drone_id, s in self._state_table.items()
                if now - s["timestamp"] < self.timeout
            ]

    def get_state(self, drone_id: int) -> dict | None:
        """
        Повертає останній відомий стан дрона або None.
        """
        with self._lock:
            return self._state_table.get(drone_id)

    def get_all_states(self) -> dict:
        """
        Повертає копію всієї таблиці станів.
        """
        with self._lock:
            return dict(self._state_table)
