"""
agent_emulator.py — Простий емулятор дрона для тестування логіки рою без SITL.
"""

import threading
import time
import random

from utils.logger import get_logger

logger = get_logger("simulation.agent_emulator")


class AgentEmulator:
    """
    Клас для імітації дрона з базовим станом та позицією.
    """

    def __init__(self, drone_id: int, update_interval=0.1):
        self.drone_id = drone_id
        self.position = [0.0, 0.0, 50.0]  # XYZ у метрах
        self.status = "idle"
        self.running = False
        self.update_interval = update_interval

        self._thread = threading.Thread(target=self._run_loop, daemon=True)

    def start(self):
        logger.info(f"[Emu {self.drone_id}] Старт емульованого дрона")
        self.running = True
        self._thread.start()

    def stop(self):
        logger.info(f"[Emu {self.drone_id}] Зупинка емуляції")
        self.running = False

    def _run_loop(self):
        """
        Цикл оновлення позиції.
        """
        while self.running:
            if self.status == "active":
                # Простий випадковий рух
                dx = random.uniform(-0.5, 0.5)
                dy = random.uniform(-0.5, 0.5)
                dz = random.uniform(-0.2, 0.2)
                self.position[0] += dx
                self.position[1] += dy
                self.position[2] = max(5.0, min(100.0, self.position[2] + dz))  # межі висоти

                logger.debug(f"[Emu {self.drone_id}] Нова позиція: {self.position}")
            time.sleep(self.update_interval)

    def set_status(self, status: str):
        """
        Встановлення статусу дрона: idle, active, holding, landing
        """
        logger.info(f"[Emu {self.drone_id}] Статус змінено на {status}")
        self.status = status

    def get_state(self):
        """
        Повертає поточний стан дрона.
        """
        return {
            "id": self.drone_id,
            "position": self.position,
            "status": self.status
        }
