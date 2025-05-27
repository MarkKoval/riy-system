"""
test_swarm_manager.py — Юніт-тести для SwarmManager.
"""

import unittest
from unittest.mock import patch, MagicMock
from core.swarm_manager import SwarmManager


class TestSwarmManager(unittest.TestCase):

    def setUp(self):
        # Мінімальна конфігурація для тестів
        self.test_config = {
            "swarm": {
                "max_drones": 3
            },
            "communication": {
                "port": 14550,
                "broadcast_address": "127.0.0.1",
                "heartbeat_interval_ms": 100
            }
        }

    @patch("core.swarm_manager.DroneAgent")
    def test_launch_swarm_creates_agents(self, mock_drone_agent):
        manager = SwarmManager(config=self.test_config)
        manager.launch_swarm()

        self.assertEqual(len(manager.agents), 3)
        self.assertEqual(mock_drone_agent.call_count, 3)
        for agent in manager.agents:
            agent.start.assert_called_once()

    @patch("core.swarm_manager.DroneAgent")
    def test_broadcast_command(self, mock_drone_agent):
        agent_mock = MagicMock()
        mock_drone_agent.return_value = agent_mock

        manager = SwarmManager(config=self.test_config)
        manager.launch_swarm()
        manager.broadcast_command("hold")

        self.assertEqual(agent_mock.communicator.send_message.call_count, 3)
        for call in agent_mock.communicator.send_message.call_args_list:
            args, _ = call
            self.assertEqual(args[0]["command"], "hold")

    @patch("core.swarm_manager.DroneAgent")
    def test_stop_swarm(self, mock_drone_agent):
        agent_mock = MagicMock()
        mock_drone_agent.return_value = agent_mock

        manager = SwarmManager(config=self.test_config)
        manager.launch_swarm()
        manager.stop_swarm()

        for agent in manager.agents:
            agent.stop.assert_called_once()


if __name__ == "__main__":
    unittest.main()
