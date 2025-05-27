"""
map_renderer.py — Віджет для відображення мапи та місій (waypoints).
"""

import customtkinter as ctk


class MapRenderer(ctk.CTkFrame):
    """
    Віджет для відображення плану місії або карти з точками.
    """

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.pack(fill="both", expand=True)

        self.canvas = ctk.CTkCanvas(self, bg="white", width=800, height=600)
        self.canvas.pack(fill="both", expand=True)

        self.scale = 5  # коефіцієнт масштабування
        self.grid_step = 20  # відстань між сітками (в пікселях)
        self.waypoints = []  # список (x, y)

        self._draw_grid()
        self.bind("<Configure>", self._on_resize)

    def _on_resize(self, event):
        self.canvas.config(width=event.width, height=event.height)
        self.redraw()

    def _draw_grid(self):
        """
        Малює координатну сітку.
        """
        self.canvas.delete("grid")

        w = int(self.canvas.winfo_width())
        h = int(self.canvas.winfo_height())

        for x in range(0, w, self.grid_step):
            self.canvas.create_line(x, 0, x, h, fill="#ddd", tags="grid")
        for y in range(0, h, self.grid_step):
            self.canvas.create_line(0, y, w, y, fill="#ddd", tags="grid")

    def set_waypoints(self, waypoints: list):
        """
        Встановлює нові точки маршруту та перемальовує.
        """
        self.waypoints = waypoints
        self.redraw()

    def redraw(self):
        """
        Перемальовує мапу: сітка + точки.
        """
        self.canvas.delete("all")
        self._draw_grid()

        r = 6
        for i, (x, y) in enumerate(self.waypoints):
            cx = 400 + x * self.scale
            cy = 300 - y * self.scale

            self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill="blue")
            self.canvas.create_text(cx, cy - 10, text=f"WP{i+1}", fill="black", font=("Arial", 10))

        # З'єднання точок лінією
        if len(self.waypoints) >= 2:
            points = [
                (400 + x * self.scale, 300 - y * self.scale)
                for (x, y) in self.waypoints
            ]
            self.canvas.create_line(points, fill="blue", width=2)

    def clear(self):
        """
        Очищає всі waypoints.
        """
        self.waypoints = []
        self.redraw()
