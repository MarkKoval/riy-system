"""
sitl_launcher.py — Модуль для запуску інстансів ArduPilot SITL з командного рядка.
"""

import subprocess
import os
import time
from utils.logger import get_logger

logger = get_logger("simulation.sitl_launcher")


class SITLLauncher:
    """
    Клас для запуску кількох екземплярів ArduPilot SITL (Software-In-The-Loop).
    """

    def __init__(self, sitl_path="~/ardupilot/Tools/autotest/sim_vehicle.py", model="quad", start_port=14550, instances=1):
        self.sitl_path = os.path.expanduser(sitl_path)
        self.model = model
        self.start_port = start_port
        self.instances = instances
        self.processes = []

    def launch_all(self):
        """
        Запускає всі інстанси SITL у фонових процесах.
        """
        logger.info(f"Запуск {self.instances} SITL дронів з моделлю '{self.model}'")

        for i in range(self.instances):
            port = self.start_port + i * 2  # порт для MAVLink: 14550, 14552, ...
            vehicle_name = f"drone{i+1}"
            process = self._launch_single_instance(instance=i, name=vehicle_name, port=port)
            self.processes.append(process)
            time.sleep(1.5)  # Пауза для стабільного запуску

        logger.info("✅ Усі інстанси SITL запущено")

    def _launch_single_instance(self, instance: int, name: str, port: int):
        """
        Запускає один інстанс SITL.
        """
        sitl_cmd = [
            self.sitl_path,
            "-v", "ArduCopter",
            "-f", self.model,
            "--instance", str(instance),
            "--out", f"udp:127.0.0.1:{port}"
        ]

        env = os.environ.copy()
        working_dir = os.path.expanduser(f"/tmp/sitl_{name}")
        os.makedirs(working_dir, exist_ok=True)

        logger.info(f"🚀 Запуск {name} [instance={instance}] на порту {port}")
        return subprocess.Popen(
            sitl_cmd,
            cwd=working_dir,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

    def stop_all(self):
        """
        Завершує всі SITL-процеси.
        """
        logger.info("⛔ Зупинка всіх SITL інстансів")
        for proc in self.processes:
            proc.terminate()
        self.processes = []
