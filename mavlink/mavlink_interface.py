"""
mavlink_interface.py — Базовий інтерфейс для підключення до дрона через MAVLink.
"""

from pymavlink import mavutil
from mavlink.command_sender import CommandSender
from mavlink.telemetry_parser import TelemetryParser
from utils.logger import get_logger

logger = get_logger("mavlink.mavlink_interface")


class MAVLinkInterface:
    """
    Інтерфейс для роботи з MAVLink-дроном: підключення, надсилання команд, отримання телеметрії.
    """

    def __init__(self, connection_string="udp:127.0.0.1:14550", system_id=1, component_id=1):
        self.connection_string = connection_string
        self.system_id = system_id
        self.component_id = component_id

        self._conn = None
        self.command = None
        self.telemetry = None

    def connect(self, wait_heartbeat=True):
        """
        Створює MAVLink-з’єднання та ініціалізує командний і телеметрійний модулі.
        """
        logger.info(f"Підключення до автопілота через {self.connection_string}")
        try:
            self._conn = mavutil.mavlink_connection(self.connection_string)
            if wait_heartbeat:
                logger.info("Очікування heartbeat...")
                self._conn.wait_heartbeat(timeout=10)
                logger.info(f"Отримано heartbeat від system {self._conn.target_system}, component {self._conn.target_component}")
        except Exception as e:
            logger.error(f"Не вдалося встановити з’єднання: {e}")
            raise

        self.command = CommandSender(self._conn, self.system_id, self.component_id)
        self.telemetry = TelemetryParser(self._conn)

    def get_connection(self):
        return self._conn

    def is_connected(self):
        return self._conn is not None and self._conn.target_system != 0
