# Automatic System (AS) "Swarm" - Quadcopter swarm control system

Automatic System (AS) “Swarm” is a decentralized platform for 3D flight mission planning and synchronized control of groups of unmanned aerial vehicles (UAVs).

## 🔧 Main features

- 3D visualization of missions with terrain and obstacles;
- Decentralized swarm management (peer-to-peer);
- Support for MAVLink protocol (ArduPilot, PX4);
- Automatic collision avoidance and formation preservation;
- Support for simulations (ArduPilot SITL).

---

## 📦 Project structure
```bash
riy-system/
├── core/                          # 🧠 Swarm logic
│   ├── __init__.py                # Initializes the core module
│   ├── communication.py           # 📡 Inter-drone communication
│   ├── failsafe.py                # 🛡️ Failsafe mechanisms
│   ├── drone_agent.py             # 🤖 Individual drone agent logic
│   ├── swarm_manager.py           # 👨‍✈️ Swarm coordination logic
│   └── state_sync.py              # 🔄 State synchronization
│
├── mavlink/                       # 🔗 MAVLink communication
│   ├── __init__.py                # Initializes the MAVLink module
│   ├── mavlink_interface.py       # 🧩 MAVLink connection wrapper
│   ├── command_sender.py          # 📤 Send commands via MAVLink
│   └── telemetry_parser.py        # 📥 Parse telemetry data
│
├── simulation/                    # 🧪 Simulation tools
│   ├── __init__.py                # Initializes the simulation module
│   ├── sitl_launcher.py           # 🚀 Launch ArduPilot SITL
│   └── agent_emulator.py          # 🛰️ Emulate drone behavior
│
├── ui/                            # 🖥️ User Interface
│   ├── gcs_gui.py                 # 🧭 GCS graphical interface
│   ├── map_widget.py              # 🗺️ Map visualization widget
│   ├── __init__.py                # Initializes the UI module
│   └── telemetry_panel.py         # 📊 Telemetry display panel
│
├── utils/                         # 🛠️ Utility functions
│   ├── __init__.py                # Initializes the utils module
│   ├── live_monitor.py            # 👀 Live status monitor
│   ├── map_renderer.py            # 🧭 Map rendering logic
│   └── mission_editor.py          # ✏️ Mission planning editor
│
├── config/                        # ⚙️ Configuration files
│   ├── system_config.yaml         # System-wide config
│   └── mission_templates/         # 📄 Mission templates
│       └── sample_mission.json    # Example mission file
│
├── tests/                         # 🧪 Unit tests
│   ├── test_mavlink_interface.py  # Test MAVLink layer
│   ├── test_swarm_manager.py      # Test swarm logic
│   └── test_ui.py                 # Test user interface
│
├── main.py                        # 🎬 Entry point for the system
├── launch.sh                      # 🚀 Simulation launch script
├── .env.example                   # 📁 Example environment variables
├── requirements.txt               # 📦 Python dependencies
└── README.md                      # 📘 Project documentation
```

---

## 🚀 Startup.

> ⚠️ Before starting, make sure you have Python 3.11+ installed

### 1. Clone the project

```bash
git clone https://github.com/MarkKoval/riy-system.git
cd riy-system
```

### 2. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
### 3. Setting up the environment
bash
Copy
Edit
cp .env.example .env
Fill in .env with your connection parameters.

### 4. Starting the system
```bash
./launch.sh
```
Or manually:
```bash
python core/swarm_manager.py
```
### 🧪 Testing
```bash
pytest tests/
```
### 🧠 Technologies
- Python 3.11

- MAVLink (via DroneKit or pymavlink)

- SITL (ArduPilot)

- customTkinter for GUI

- UDP Broadcast, Wi-Fi/LoRa

### 📁 Configuration example
yaml
#### config/system_config.yaml
swarm:
 max_drones: 20
 default_altitude: 50
 communication_protocol: "udp"
 simulation_mode: true
### 🧑‍💻 Author
- Koval Mark Andriyovych KN-412, Lviv Polytechnic
- Supervisor: Kolesnyk K.K. 
