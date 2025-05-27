"""
command_sender.py — Модуль для надсилання MAVLink-команд до дронів.
"""

from pymavlink import mavutil
from utils.logger import get_logger

logger = get_logger("mavlink.command_sender")


class CommandSender:
    """
    Відправник команд MAVLink до автопілота.
    """

    def __init__(self, connection: mavutil.mavlink_connection, target_system=1, target_component=1):
        self.conn = connection
        self.target_system = target_system
        self.target_component = target_component

    def arm(self):
        """
        Озброєння двигунів.
        """
        logger.info("Надсилаємо ARM команду")
        self.conn.mav.command_long_send(
            self.target_system,
            self.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0,
            1, 0, 0, 0, 0, 0, 0
        )

    def disarm(self):
        """
        Роззброєння двигунів.
        """
        logger.info("Надсилаємо DISARM команду")
        self.conn.mav.command_long_send(
            self.target_system,
            self.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0,
            0, 0, 0, 0, 0, 0, 0
        )

    def set_mode(self, mode: str):
        """
        Встановлює режим польоту (наприклад: GUIDED, AUTO, LOITER).
        """
        logger.info(f"Встановлення режиму: {mode}")
        mode_id = self._get_mode_id(mode)
        if mode_id is None:
            logger.error(f"Невідомий режим: {mode}")
            return

        self.conn.mav.set_mode_send(
            self.target_system,
            mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
            mode_id
        )

    def takeoff(self, altitude: float = 10):
        """
        Команда взльоту на вказану висоту.
        """
        logger.info(f"Команда взльоту до {altitude}м")
        self.conn.mav.command_long_send(
            self.target_system,
            self.target_component,
            mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
            0,
            0, 0, 0, 0, 0, 0,
            altitude
        )

    def land(self):
        """
        Команда посадки.
        """
        logger.info("Команда посадки")
        self.conn.mav.command_long_send(
            self.target_system,
            self.target_component,
            mavutil.mavlink.MAV_CMD_NAV_LAND,
            0,
            0, 0, 0, 0, 0, 0, 0
        )

    def _get_mode_id(self, mode: str):
        """
        Повертає числовий ID режиму з текстової назви.
        """
        self.conn.wait_heartbeat()
        modes = self.conn.mode_mapping()
        return modes.get(mode.upper())
