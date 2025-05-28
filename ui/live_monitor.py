"""
live_monitor.py — Модуль для візуального моніторингу рою в реальному часі.
"""

import customtkinter as ctk
import threading
import time
import random


class LiveMonitor(ctk.CTkFrame):
    """
    Віджет для моніторингу позицій дронів у реальному часі.
    """

    def __init__(self, master=None, swarm_data_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.pack(fill="both", expand=True)

        self.canvas = ctk.CTkCanvas(self, bg="black", width=800, height=600)
        self.canvas.pack(fill="both", expand=True)

        self.running = True
        self.drones = {}  # drone_id -> canvas_object
        self.swarm_data_callback = swarm_data_callback or self._mock_data

        self.update_thread = threading.Thread(target=self._update_loop, daemon=True)
        self.update_thread.start()

    def _update_loop(self):
        """
        Оновлює позиції дронів кожні 100 мс.
        """
        while self.running:
            data = self.swarm_data_callback()
            self._render_swarm(data)
            time.sleep(0.1)

    def _render_swarm(self, drone_states: dict):
        """
        Відображає позиції дронів на канві.
        """
        self.canvas.delete("all")
        for drone_id, state in drone_states.items():
            try:
                x = float(state["position"]["x"])
                y = float(state["position"]["y"])
            except (ValueError, TypeError, KeyError):
                x, y = 0, 0  # fallback, якщо значення некоректне

            screen_x = 400 + x * 5  # маштабування
            screen_y = 300 - y * 5
            r = 10
            self.canvas.create_oval(
                screen_x - r, screen_y - r, screen_x + r, screen_y + r,
                fill="cyan", outline="white"
            )
            self.canvas.create_text(
                screen_x, screen_y - 15,
                text=f"ID {drone_id}", fill="white", font=("Arial", 10)
            )

    def stop(self):
        """
        Зупиняє оновлення монітору.
        """
        self.running = False

    def _mock_data(self):
        """
        Демонстраційні дані для автономного режиму.
        """
        return {
            i: {
                "position": [random.uniform(-20, 20), random.uniform(-20, 20), 50],
                "status": "active"
            }
            for i in range(1, 6)
        }
