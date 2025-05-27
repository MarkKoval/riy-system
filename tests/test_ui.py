"""
test_ui.py — Юніт-тести для UI-компонентів.
"""

import unittest
from unittest.mock import patch, MagicMock


class TestMissionEditor(unittest.TestCase):

    @patch("ui.mission_editor.tk")
    def test_mission_editor_init(self, mock_tk):
        from ui.mission_editor import MissionEditor

        mock_root = MagicMock()
        editor = MissionEditor(mock_root)

        self.assertIsNotNone(editor)
        mock_tk.Label.assert_called()  # базова перевірка, що елементи створюються


class TestLiveMonitor(unittest.TestCase):

    @patch("ui.live_monitor.tk")
    def test_live_monitor_display(self, mock_tk):
        from ui.live_monitor import LiveMonitor

        mock_root = MagicMock()
        monitor = LiveMonitor(mock_root)

        self.assertIsNotNone(monitor)
        mock_tk.Canvas.assert_called()  # перевірка побудови канви (карти)


if __name__ == "__main__":
    unittest.main()
