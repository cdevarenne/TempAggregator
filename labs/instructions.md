# Instructions

## What To Expect

- We'll be building the solution together in real-time during our interview session
- You're welcome to review the problem and think through your approach beforehand, but we'll write the code collaboratively during the interview
- Feel free to use whatever tools are part of your normal workflow - including AI assistants if that's how you typically work
- We'll be working together with screen sharing, and we'd love for you to explain your thinking as we go
- Ask questions anytime! We're interested in understanding your problem-solving approach and how you think through challenges

## Setup

- Please have Python 3 and your preferred development environment ready
- Make sure you're set up for screen sharing
- Attached: `sensor_aggregator.py` (starter code) and `async_bonus.py` (optional bonus)

---

## Sensor Reading Aggregator - Interview Question

### Problem Statement

You're working with real-time sensor data from IoT devices. Your task is to write a function that groups consecutive sensor readings by device and detects when readings are stable (within a threshold).

> [!IMPORTANT]
> "Consecutive" means consecutive in the input list order. When the `device_id` changes, start a new group.

**Input Format**

You'll receive a list of sensor readings, where each reading is a dictionary with:
- timestamp: Unix timestamp in seconds (integer) - represents when the reading was taken
- device_id: String identifier for the sensor
- value: Float representing the sensor measurement (e.g., temperature in Celsius)

The input is sorted by timestamp.

---

**Example Input**

``` json
readings = [
    {"timestamp": 1698000000, "device_id": "sensor_1", "value": 23.5},
    {"timestamp": 1698000005, "device_id": "sensor_1", "value": 23.7},
    {"timestamp": 1698000010, "device_id": "sensor_2", "value": 45.2},
    {"timestamp": 1698000015, "device_id": "sensor_1", "value": 28.1},
    {"timestamp": 1698000055, "device_id": "sensor_1", "value": 31.5},
    {"timestamp": 1698000060, "device_id": "sensor_2", "value": 45.8},
    {"timestamp": 1698000065, "device_id": "sensor_2", "value": 46.1},
]
```
---

**Expected Output**

Group consecutive readings from the same device (in input list order). For each group, calculate:
- The device ID
- List of values from the readings
- Start timestamp (first reading in group)
- End timestamp (last reading in group)
- Whether the readings are "stable" (all temperature values within ±1.0 degrees of each other)

``` json
[
    {
        "device_id": "sensor_1",
        "readings": [23.5, 23.7],
        "start_time": 1698000000,
        "end_time": 1698000005,
        "is_stable": True  # 23.7 - 23.5 = 0.2, within 1.0
    },
    {
        "device_id": "sensor_2",
        "readings": [45.2],
        "start_time": 1698000010,
        "end_time": 1698000010,
        "is_stable": True  # Single reading is always stable
    },
    {
        "device_id": "sensor_1",
        "readings": [28.1, 31.5],
        "start_time": 1698000015,
        "end_time": 1698000055,
        "is_stable": False  # 31.5 - 28.1 = 3.4, exceeds 1.0
    },
    {
        "device_id": "sensor_2",
        "readings": [45.8, 46.1],
        "start_time": 1698000060,
        "end_time": 1698000065,
        "is_stable": True  # 46.1 - 45.8 = 0.3, within 1.0
    }
]
```
---

### Requirements

1. Group consecutive readings from the same device (consecutive in the input list)
2. Calculate the stability of each group (stable if max_value - min_value <= 1.0 degrees)
3. Track start and end timestamps for each group

Feel free to ask clarifying questions as you work through the problem.

