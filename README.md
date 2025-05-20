# 🐶 SmartBowl – IoT-Based Smart Pet Feeder

SmartBowl is a smart pet feeding system built using Python and IoT technologies. It ensures pets are fed regularly and intelligently, combining automation, sensors, and a clean user interface.

> 🎯 Designed for pet owners who want to automate feeding while tracking their pets’ habits.

## ✨ Features

| Feature | Description |
|--------|-------------|
| 🕹️ Manual Feeding | Feed your pet instantly via a GUI button |
| ⏰ Scheduled Feeding | Set feeding times for morning, noon, and evening |
| 🧠 Adaptive Feeding | Learns your pet’s eating habits and adjusts portion size |
| 🎙️ Bark Detection | Auto-feeds when barking is detected and bowl is under 50% full |
| 📊 GUI Dashboard | Displays real-time feeding status and last meal |
| 🧪 Fullness Sensor | Prevents overfeeding with a bowl-level detector |
| 📁 Data Logging | Stores feeding history in a local SQLite database |

## 🧰 Tech Stack

- 🐍 Python 3
- 🖥️ PyQt5 (GUI)
- ☁️ MQTT Protocol (`paho-mqtt`)
- 🗃️ SQLite3 (Local DB)
- 🎧 Audio/image resources

## 🗂️ Project Structure

| File | Purpose |
|------|---------|
| `PetFeederGui.py` | Main graphical interface |
| `FeedingSchedulerGui.py` | Feeding time scheduler |
| `ManualFeedButton.py` | Manual feeding interface |
| `autoFeeder.py` | Handles automated feeding logic |
| `FeederRelay.py` | Controls the relay triggering the feeder |
| `BowlFullSensor.py` | Simulates detection of full bowl |
| `PetFeederDataManager.py` | Manages feeding data and logs |
| `create_db.py` | Initializes the SQLite database |
| `mqtt_init.py` | MQTT client configuration |
| `view_schedule.py` | GUI to review and edit feed schedules |



## ▶️ How to Run

1. Prerequisites:
- Python 3.x installed on your system  
- MQTT broker (like HiveMQ or Mosquitto, optional for local tests)
2. Install requirements:
```
pip install PyQt5 paho-mqtt
```
3.Initialize the database:
```
python create_db.py
```
4.Run the main GUI:
```
python PetFeederGui.py
```
## 👩‍💻 Developed by

- [Shir Berko](https://github.com/ShirBerko)  
- [Michelle Cain](https://github.com/michellecain31)  
- [Tal Itzhak](https://github.com/TalItzhak3)

