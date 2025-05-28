"""
drone_agent.py — Логіка окремого агента-дрона в рої.
"""

import threading
import time
import random
from core.communication import Communication
from core.communication import DroneCommunicator
from utils.logger import get_logger

logger = get_logger("core.drone_agent")





class DroneAgent:
    """
    Агент, який представляє одного дрона у рої.
    """
    

    def __init__(self, drone_id, communicator=None, mavlink=None, config=None, port=14550):
        self.config = config
        self.drone_id = drone_id
        self.communicator = communicator
        self.mavlink = mavlink
        self.port = port

        self.state = {
            "drone_id": self.drone_id,
            "battery": random.randint(70, 100),
            "position": {"x": random.uniform(0, 100), "y": random.uniform(0, 100), "z": random.uniform(0, 20)},
            "role": "лідер" if self.drone_id == 1 else "послідовник",
            "status": "active"
        }

        # Ініціалізація комунікації
        comm_cfg = self.config.get("communication", {})
        self.communicator = DroneCommunicator(
            port=comm_cfg.get("port", 14550),
            broadcast_ip=comm_cfg.get("broadcast_address", "192.168.1.255"),
            drone_id=self.drone_id,
            heartbeat_interval_ms=comm_cfg.get("heartbeat_interval_ms", 100)
        )

        self.state = {
            "id": self.drone_id,
            "position": [0.0, 0.0, self.config["swarm"].get("default_altitude", 50)],
            "status": "idle",
            "last_heartbeat": time.time(),
            "position": {"x": 0, "y": 0, "z": 0},
        }

        self._main_thread = threading.Thread(target=self._run_loop, daemon=True)

    def start(self):
        logger.info(f"[Drone {self.drone_id}] Агент стартує.")
        
        self.communicator = Communication(
            drone_id=self.drone_id,
            port=self.port  # <=== правильний порт для кожного
        )
        self.communicator.start()

    def stop(self):
        logger.info(f"[Drone {self.drone_id}] Агент зупиняється.")
        self.running = False
        self.communicator.stop()

    def _run_loop(self):
        """
        Основний цикл: обробка вхідних повідомлень, оновлення стану.
        """
        while self.running:
            messages = self.communicator.fetch_received()
            for msg in messages:
                self._handle_message(msg)

            self._simulate_position_update()
            time.sleep(0.1)

    def _handle_message(self, message: dict):
        """
        Обробка вхідного повідомлення від іншого дрона.
        """
        msg_type = message.get("type")
        sender_id = message.get("sender_id")

        if msg_type == "heartbeat":
            logger.debug(f"[Drone {self.drone_id}] Heartbeat від {sender_id}")
        elif msg_type == "command":
            command = message.get("command")
            logger.info(f"[Drone {self.drone_id}] Отримано команду: {command} від {sender_id}")
            self._execute_command(command)
        elif msg_type == "mission":
            self.mission = message.get("waypoints", [])
            self.state["status"] = "executing"
        else:
            logger.warning(f"[Drone {self.drone_id}] Невідомий тип повідомлення: {msg_type}")

    def _execute_command(self, command: str):
        """
        Реакція на вхідні команди (статус або рух).
        """
        if command == "hold":
            self.state["status"] = "holding"
        elif command == "resume":
            self.state["status"] = "active"
        elif command == "land":
            self.state["status"] = "landing"
        else:
            logger.warning(f"[Drone {self.drone_id}] Невідома команда: {command}")

    def _simulate_position_update(self):
        """
        Симуляція оновлення позиції (тільки для тестів/розробки).
        """
        if self.state["status"] == "active":
            self.state["position"][0] += 0.1  # рух по X
            self.state["position"][1] += 0.05  # рух по Y
            logger.debug(f"[Drone {self.drone_id}] Нова позиція: {self.state['position']}")
