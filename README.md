# AS "Swarm" - Quadcopter swarm control system

**AS “Swarm” is a decentralized platform for 3D flight mission planning and synchronized control of groups of unmanned aerial vehicles (UAVs).

## 🔧 Main features

- 3D visualization of missions with terrain and obstacles;
- Decentralized swarm management (peer-to-peer);
- Support for MAVLink protocol (ArduPilot, PX4);
- Automatic collision avoidance and formation preservation;
- Support for simulations (ArduPilot SITL).

---

## 📦 Project structure

- `core/` - swarm logic, agents, synchronization
- `mavlink/` - interaction with the autopilot via MAVLink
- `ui/` - user interface for planning and monitoring
- `simulation/` - run SITL simulations and test agents
- `config/` - system configuration files
- `utils/` - auxiliary utilities
- `tests/` - automated tests

---

## 🚀 Startup.

> ⚠️ Before starting, make sure you have Python 3.11+ installed

### 1. Clone the project

```bash
git clone https://github.com/your-name/riy-system.git
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