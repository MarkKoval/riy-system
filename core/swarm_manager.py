"""
swarm_manager.py — Головний керуючий модуль для запуску та координації рою дронів.
"""

import time
from core.drone_agent import DroneAgent
from mavlink.mavlink_interface import MAVLinkInterface
from utils.logger import get_logger

logger = get_logger("core.swarm_manager")


class SwarmManager:
    """
    Менеджер рою: ініціалізує агентів, координує місії, розподіляє команди.
    """

    def __init__(self, config: dict):
        self.config = config
        self.agents: list[DroneAgent] = []
        self.max_drones = config.get("swarm", {}).get("max_drones", 5)
        self.simulation_mode = config.get("simulation", {}).get("enabled", True)
        self.use_emulator = config.get("simulation", {}).get("use_emulator", True)
        self.start_port = config.get("communication", {}).get("port", 14550)
        self.host = config.get("communication", {}).get("host", "127.0.0.1")

    def launch_swarm(self):
        """
        Ініціалізує та запускає всіх агентів рою.
        """
        mode = "емуляції" if self.use_emulator else "SITL"
        logger.info(f"Запуск {self.max_drones} дронів у режимі {mode}")

        for i in range(self.max_drones):
            drone_id = i + 1
            port = self.start_port + i * 2
        
            if self.use_emulator:
                mav = None
            else:
                mav = MAVLinkInterface(udp_port=port)
        
            agent = DroneAgent(
                drone_id=drone_id,
                mavlink=mav,
                config=self.config,
                port=port  # <=== додано
            )
            agent.start()
            self.agents.append(agent)
            time.sleep(0.1)

        logger.info("✅ Усі агенти успішно запущені.")

    def broadcast_command(self, command: str):
        """
        Надсилає команду всім агентам у роєвій мережі.
        """
        logger.info(f"📡 Трансляція команди '{command}' всім дронам.")
        for agent in self.agents:
            if agent.communicator:
                agent.communicator.send_message({
                    "type": "command",
                    "command": command
                })

    def broadcast_mission(self, waypoints):
        """
        Передає місію всім дронам.
        """
        logger.info("📦 Відправка місії всім агентам.")
        for agent in self.agents:
            if agent.communicator:
                agent.communicator.send_message({
                    "type": "mission",
                    "waypoints": waypoints
                })

    def run_mission_loop(self):
        """
        Простий демонстраційний цикл місії.
        """
        try:
            while True:
                time.sleep(10)
                self.broadcast_command("hold")
                time.sleep(5)
                self.broadcast_command("resume")
        except KeyboardInterrupt:
            logger.warning("🛑 Отримано Ctrl+C — завершення роботи рою.")
            self.stop_swarm()

    def get_swarm_state(self):
        """
        Повертає стан усіх дронів.
        """
        return {a.drone_id: a.state for a in self.agents}

    def stop_swarm(self):
        """
        Зупиняє всіх агентів рою.
        """
        logger.info("⛔ Зупинка всіх агентів рою.")
        for agent in self.agents:
            agent.stop()
