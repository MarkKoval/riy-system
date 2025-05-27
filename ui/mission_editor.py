"""
mission_editor.py — Графічний редактор для створення та керування місіями.
"""

import customtkinter as ctk
from ui.map_renderer import MapRenderer


class MissionEditor(ctk.CTkFrame):
    """
    Головний віджет для створення маршруту дронів.
    """

    def __init__(self, master=None, mission_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.pack(fill="both", expand=True)

        self.mission_callback = mission_callback or self._default_mission_callback
        self.waypoints = []

        self._build_ui()

    def _build_ui(self):
        """
        Створення елементів інтерфейсу.
        """
        self.map = MapRenderer(self)
        self.map.pack(fill="both", expand=True)

        control_frame = ctk.CTkFrame(self)
        control_frame.pack(fill="x", padx=10, pady=10)

        self.x_input = ctk.CTkEntry(control_frame, placeholder_text="X")
        self.x_input.pack(side="left", padx=5)

        self.y_input = ctk.CTkEntry(control_frame, placeholder_text="Y")
        self.y_input.pack(side="left", padx=5)

        add_btn = ctk.CTkButton(control_frame, text="➕ Додати точку", command=self._add_waypoint)
        add_btn.pack(side="left", padx=5)

        clear_btn = ctk.CTkButton(control_frame, text="🗑 Очистити", command=self._clear_mission)
        clear_btn.pack(side="left", padx=5)

        send_btn = ctk.CTkButton(control_frame, text="🚀 Запустити місію", command=self._send_mission)
        send_btn.pack(side="right", padx=5)

    def _add_waypoint(self):
        """
        Додає точку до місії.
        """
        try:
            x = float(self.x_input.get())
            y = float(self.y_input.get())
            self.waypoints.append((x, y))
            self.map.set_waypoints(self.waypoints)
            self.x_input.delete(0, "end")
            self.y_input.delete(0, "end")
        except ValueError:
            print("Некоректні координати")

    def _clear_mission(self):
        """
        Очищення місії.
        """
        self.waypoints = []
        self.map.clear()

    def _send_mission(self):
        """
        Надсилання місії у зовнішній компонент (наприклад, SwarmManager).
        """
        if self.waypoints:
            self.mission_callback(self.waypoints)

    def _default_mission_callback(self, waypoints):
        """
        Стандартна обробка (для дебагу).
        """
        print("Місія передана:", waypoints)
