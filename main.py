# main.py — повний запуск системи "Рій"

import os
import threading
from core import config, logger
from core.swarm_manager import SwarmManager
from simulation.sitl_launcher import SITLLauncher
from simulation.agent_emulator import AgentEmulator
import customtkinter as ctk
from ui.mission_editor import MissionEditor
from ui.live_monitor import LiveMonitor

# --- INIT CONFIG ---
cfg = config

# --- OPTIONAL: Launch SITL if enabled ---
if cfg.get("simulation", {}).get("enabled") and not cfg.get("simulation", {}).get("use_emulator", True):
    sitl = SITLLauncher(
        sitl_path=cfg["simulation"]["sitl_path"],
        model=cfg["simulation"]["model"],
        start_port=cfg["communication"]["port"],
        instances=cfg["simulation"]["instances"]
    )
    sitl.launch_all()

# --- Launch SwarmManager ---
swarm = SwarmManager(cfg)
swarm_thread = threading.Thread(target=lambda: (
    swarm.launch_swarm(),
    swarm.run_mission_loop()
), daemon=True)
swarm_thread.start()

# --- Launch GUI (Live Monitor + Mission Editor) ---
def start_gui():
    import customtkinter as ctk
    from tkinter import StringVar

    app = ctk.CTk()
    app.title("АС 'РІЙ' — Система керування роєм дронів")
    app.geometry("1200x850")

    # === ГОЛОВНЕ МЕНЮ У ВИГЛЯДІ ВКЛАДОК ===
    tabs = ctk.CTkTabview(master=app)
    tabs.pack(fill="both", expand=True, padx=10, pady=10)

    # === ВКЛАДКА: КАРТА (LiveMonitor) ===
    tab_map = tabs.add("🗺 Карта")
    monitor = LiveMonitor(master=tab_map, swarm_data_callback=swarm.get_swarm_state)
    monitor.pack(fill="both", expand=True)

    # === ВКЛАДКА: ДРОНИ (Всі дрони одночасно) ===
    tab_drones = tabs.add("🛩 Дрони")

    drones_list_frame = ctk.CTkScrollableFrame(tab_drones)
    drones_list_frame.pack(fill="both", expand=True, padx=10, pady=10)

    drone_labels = {}  # ключ: drone_id, значення: CTkLabel

    def update_all_drone_info():

        

        for widget in drones_list_frame.winfo_children():
            widget.destroy()

        for agent in swarm.agents:
            state = agent.state
            drone_id = state.get("drone_id", "N/A")
            battery = state.get("battery", "N/A")
            coords = state.get("position", {"x": 0, "y": 0, "z": 0})
            role = state.get("role", "невідомо")
            status = state.get("status", "невідомо")

            text = (
                f"🆔 Дрон {drone_id}  —  "
                f"📡 Статус: {status}  |  "
                f"🎯 Роль: {role}  |  "
                f"🔋 {battery}%  |  "
                f"📍 X={coords.get('x', 0)} Y={coords.get('y', 0)} Z={coords.get('z', 0)}"
            )

            label = ctk.CTkLabel(drones_list_frame, text=text, anchor="w", justify="left")
            label.pack(fill="x", pady=2, padx=5)

        # Повторно оновлювати кожні 3 секунди
        tab_drones.after(3000, update_all_drone_info)

        if not swarm.agents:
            empty_label = ctk.CTkLabel(drones_list_frame, text="🔌 Дрони ще не підключені...")
            empty_label.pack(pady=10)
            tab_drones.after(3000, update_all_drone_info)
        return

    update_all_drone_info()

    # === ВКЛАДКА: ПЛАНУВАЛЬНИК МІСІЙ ===
    tab_missions = tabs.add("📋 Планувальник")
    editor = MissionEditor(
        master=tab_missions,
        mission_callback=swarm.broadcast_mission,
        width=600,
        height=400
    )
    editor.pack(pady=20, padx=20)


    # === ВКЛАДКА: НАЛАШТУВАННЯ ===
    tab_settings = tabs.add("⚙️ Налаштування")
    ctk.CTkLabel(tab_settings, text="(тут будуть налаштування системи)").pack(pady=20)

    # === СТАТУС-БАР ВНИЗУ ===
    status_bar = ctk.CTkFrame(master=app, height=40)
    status_bar.pack(side="bottom", fill="x")
    mav_label = ctk.CTkLabel(status_bar, text="🔌 MAVLink: перевірка...", anchor="w")
    mav_label.pack(side="left", padx=10)
    telemetry_label = ctk.CTkLabel(status_bar, text="📶 Телеметрія: невідомо", anchor="e")
    telemetry_label.pack(side="right", padx=10)

    def update_status_bar():
        try:
            connected = all(agent.mavlink.connected for agent in swarm.agents)
            if connected:
                mav_label.configure(text="🔌 MAVLink: з’єднано", text_color="green")
            else:
                mav_label.configure(text="🔌 MAVLink: ❌ немає з’єднання", text_color="red")
        except Exception:
            mav_label.configure(text="🔌 MAVLink: ⚠️ помилка", text_color="orange")

        states = swarm.get_swarm_state()
        if any("position" in s for s in states.values()):
            telemetry_label.configure(text="📶 Телеметрія: активна", text_color="green")
        else:
            telemetry_label.configure(text="📶 Телеметрія: немає даних", text_color="red")

        app.after(2000, update_status_bar)

    update_status_bar()
    app.mainloop()



start_gui()
