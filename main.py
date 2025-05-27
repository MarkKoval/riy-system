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
    app = ctk.CTk()
    app.title("АС 'РІЙ' — Керування роєм дронів")
    app.geometry("1000x800")

    monitor = LiveMonitor(master=app, swarm_data_callback=swarm.get_swarm_state)
    monitor.pack(side="left", fill="both", expand=True)

    editor = MissionEditor(master=app, mission_callback=swarm.broadcast_mission)
    editor.pack(side="right", fill="y", padx=10)

    app.mainloop()

start_gui()
