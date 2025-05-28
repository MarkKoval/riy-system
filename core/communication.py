"""
communication.py — Модуль для peer-to-peer обміну повідомленнями між дронами.
"""

import socket
import threading
import json
import time

from utils.logger import get_logger

logger = get_logger("core.communication")


class DroneCommunicator:
    """
    Клас для обміну повідомленнями між дронами через UDP broadcast або multicast.
    """

    def __init__(self, port: int, broadcast_ip: str, drone_id: int, heartbeat_interval_ms: int = 100):
        self.port = port
        self.broadcast_ip = broadcast_ip
        self.drone_id = drone_id
        self.heartbeat_interval = heartbeat_interval_ms / 1000.0
        self.running = False

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self._socket.bind(("", self.port))

        self._receive_thread = threading.Thread(target=self._receive_loop, daemon=True)
        self._heartbeat_thread = threading.Thread(target=self._heartbeat_loop, daemon=True)

        self.received_messages = []  # список вхідних повідомлень (можна замінити на чергу)

    def start(self):
        self.running = True
        self._receive_thread.start()
        self._heartbeat_thread.start()
        logger.info(f"[Drone {self.drone_id}] Комунікація запущена на порті {self.port}")

    def stop(self):
        self.running = False
        self._socket.close()
        logger.info(f"[Drone {self.drone_id}] Комунікація зупинена")

    def send_message(self, data: dict):
        """
        Надсилання повідомлення всім іншим дронам у мережі.
        """
        data["sender_id"] = self.drone_id
        try:
            raw = json.dumps(data).encode("utf-8")
            self._socket.sendto(raw, (self.broadcast_ip, self.port))
        except Exception as e:
            logger.error(f"Помилка надсилання повідомлення: {e}")

    def _receive_loop(self):
        """
        Прослуховування вхідних UDP-повідомлень.
        """
        while self.running:
            try:
                data, _ = self._socket.recvfrom(2048)
                message = json.loads(data.decode("utf-8"))
                if message.get("sender_id") != self.drone_id:
                    self.received_messages.append(message)
                    logger.debug(f"[Drone {self.drone_id}] Отримано повідомлення: {message}")
            except Exception as e:
                logger.warning(f"Помилка прийому: {e}")

    def _heartbeat_loop(self):
        """
        Періодичне надсилання heartbeat-повідомлень до інших дронів.
        """
        while self.running:
            self.send_message({
                "type": "heartbeat",
                "timestamp": time.time()
            })
            time.sleep(self.heartbeat_interval)

    def fetch_received(self) -> list:
        """
        Повертає список отриманих повідомлень та очищає буфер.
        """
        messages = self.received_messages.copy()
        self.received_messages.clear()
        return messages
