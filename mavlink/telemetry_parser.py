"""
telemetry_parser.py — Модуль для обробки вхідної телеметрії від дрона через MAVLink.
"""

from pymavlink import mavutil
from utils.logger import get_logger

logger = get_logger("mavlink.telemetry_parser")


class TelemetryParser:
    """
    Клас для зчитування телеметрії з MAVLink-з’єднання.
    """

    def __init__(self, connection: mavutil.mavlink_connection):
        self.conn = connection

    def receive_once(self):
        """
        Зчитує одне повідомлення MAVLink, якщо воно є.
        """
        msg = self.conn.recv_match(blocking=False)
        if msg:
            logger.debug(f"[Telemetry] Отримано повідомлення: {msg.get_type()}")
        return msg

    def get_position(self):
        """
        Повертає координати дрона у форматі (lat, lon, alt), якщо доступні.
        """
        msg = self.conn.recv_match(type='GLOBAL_POSITION_INT', blocking=False)
        if not msg:
            return None
        lat = msg.lat / 1e7
        lon = msg.lon / 1e7
        alt = msg.alt / 1000.0  # в метрах
        return (lat, lon, alt)

    def get_attitude(self):
        """
        Повертає крен, тангаж, курс (roll, pitch, yaw) у радіанах.
        """
        msg = self.conn.recv_match(type='ATTITUDE', blocking=False)
        if not msg:
            return None
        return (msg.roll, msg.pitch, msg.yaw)

    def get_heartbeat(self):
        """
        Зчитує повідомлення типу HEARTBEAT (можна використати для статусу).
        """
        return self.conn.recv_match(type='HEARTBEAT', blocking=False)

    def get_status_text(self):
        """
        Зчитує статусні повідомлення (debug/info/error).
        """
        msg = self.conn.recv_match(type='STATUSTEXT', blocking=False)
        if msg:
            logger.info(f"[StatusText] {msg.severity}: {msg.text}")
        return msg

    def stream_loop(self, callback=None):
        """
        Запускає нескінченний цикл, у якому передає вхідні повідомлення у callback-функцію.
        """
        while True:
            msg = self.receive_once()
            if msg and callback:
                callback(msg)
