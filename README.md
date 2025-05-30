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

riy-system/
├── core/                          # Swarm logic
│   ├── __ init __.py              # Initializes the core module
│   ├── communication.py           # Handles inter-drone communication
│   ├── failsafe.py                # Failsafe mechanisms for fault tolerance
│   ├── drone_agent.py             # Logic for individual drone agents
│   ├── swarm_manager.py           # Centralized control of the swarm
│   └── state_sync.py              # Synchronizes state across the swarm
│
├── mavlink/                       # MAVLink communication
│   ├── __ init __.py              # Initializes the MAVLink module
│   ├── mavlink_interface.py       # Wrapper for MAVLink connection
│   ├── command_sender.py          # Sends MAVLink commands to drones
│   └── telemetry_parser.py        # Parses incoming telemetry data
│
├── simulation/                    # Simulation tools
│   ├── __ init __.py              # Initializes the simulation module
│   ├── sitl_launcher.py           # Launches SITL emulation (ArduPilot)
│   └── agent_emulator.py          # Simulates drone agent behavior
│
├── ui/                            # User interface
│   ├── __ init __.py              # Initializes the UI module
│   ├── gcs_gui.py                 # Main GUI for Ground Control Station
│   ├── map_widget.py              # Map widget for visualizing drones
│   └── telemetry_panel.py         # Panel displaying telemetry data
│
├── utils/                         # Utility functions and helpers
│   ├── __ init __.py              # Initializes the utils module
│   ├── live_monitor.py            # Live status monitoring tools
│   ├── map_renderer.py            # Renders drone positions on the map
│   └── mission_editor.py          # Editor for mission planning
│
├── config/                        # Configuration files
│   ├── system_config.yaml         # System-wide configuration settings
│   └── mission_templates/         # Predefined mission plans
│       └── sample_mission.json    # Example mission definition
│
├── tests/                         # Unit tests
│   ├── test_mavlink_interface.py  # Tests for MAVLink connection logic
│   ├── test_swarm_manager.py      # Tests for swarm control and logic
│   └── test_ui.py                 # Tests for GUI components
│
├── main.py                        # Entry point for launching the system
├── launch.sh                      # Script for launching full simulation
├── .env.example                   # Example environment variables file
├── requirements.txt               # Python dependencies
└── README.md                      # Project documentation


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
