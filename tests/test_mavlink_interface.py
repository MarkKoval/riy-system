"""
test_mavlink_interface.py — Юніт-тести для MavlinkInterface.
"""

import unittest
from unittest.mock import MagicMock, patch

from mavlink.mavlink_interface import MavlinkInterface
from mavlink.command_sender import CommandSender


class TestMavlinkInterface(unittest.TestCase):

    @patch("mavlink.mavlink_interface.mavutil.mavlink_connection")
    def test_connect_successful(self, mock_connection):
        # Мок з’єднання
        mock_conn = MagicMock()
        mock_conn.wait_heartbeat.return_value = True
        mock_conn.target_system = 1
        mock_conn.target_component = 1
        mock_connection.return_value = mock_conn

        # Створення інтерфейсу
        mav = MavlinkInterface("udp:127.0.0.1:14550")
        mav.connect()

        # Перевірки
        mock_connection.assert_called_once_with("udp:127.0.0.1:14550")
        mock_conn.wait_heartbeat.assert_called_once()

        self.assertIsInstance(mav.command, CommandSender)
        self.assertTrue(mav.is_connected())

    @patch("mavlink.mavlink_interface.mavutil.mavlink_connection")
    def test_connect_fails(self, mock_connection):
        mock_connection.side_effect = Exception("Connection failed")

        mav = MavlinkInterface("udp:127.0.0.1:9999")

        with self.assertRaises(Exception) as context:
            mav.connect()

        self.assertIn("Connection failed", str(context.exception))

    @patch("mavlink.mavlink_interface.mavutil.mavlink_connection")
    def test_get_connection(self, mock_connection):
        mock_conn = MagicMock()
        mock_conn.target_system = 1
        mock_conn.target_component = 1
        mock_connection.return_value = mock_conn

        mav = MavlinkInterface("udp:127.0.0.1:14550")
        mav.connect()
        conn = mav.get_connection()

        self.assertEqual(conn, mav._conn)


if __name__ == "__main__":
    unittest.main()
