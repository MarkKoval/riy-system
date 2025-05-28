"""
swarm_manager.py — Головний керуючий модуль для запуску та координації рою дронів.
"""

import time
from core.drone_agent import DroneAgent
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

    def launch_swarm(self):
        """
        Ініціалізує та запускає всіх агентів рою.
        """
        logger.info(f"Запуск {self.max_drones} дронів у {'симуляції' if self.simulation_mode else 'реальному режимі'}")

        for i in range(self.max_drones):
            agent = DroneAgent(config=self.config, drone_id=i + 1)
            agent.start()
            self.agents.append(agent)
            time.sleep(0.1)  # невелика затримка між стартами

        logger.info("Усі агенти успішно запущені.")

    def broadcast_command(self, command: str):
        """
        Надсилає команду всім агентам у роєвій мережі.
        """
        logger.info(f"Трансляція команди '{command}' всім дронам.")
        for agent in self.agents:
            agent.communicator.send_message({
                "type": "command",
                "command": command
            })

    def get_swarm_state(self):
        return {a.drone_id: a.state for a in self.agents}


    def stop_swarm(self):
        """
        Зупиняє роботу всіх агентів.
        """
        logger.info("Зупинка всіх агентів рою.")
        for agent in self.agents:
            agent.stop()

    def run_mission_loop(self):
        """
        Прототип: основний цикл місії (може замінюватись користувачем).
        """
        try:
            while True:
                time.sleep(10)
                self.broadcast_command("hold")
                time.sleep(5)
                self.broadcast_command("resume")
        except KeyboardInterrupt:
            logger.warning("Отримано Ctrl+C — завершення роботи рою.")
            self.stop_swarm()

    def broadcast_mission(self, waypoints):
        for agent in self.agents:
            agent.communicator.send_message({
                "type": "mission",
                "waypoints": waypoints
            })

