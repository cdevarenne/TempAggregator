"""
Sensor Reading Aggregator

Groups consecutive sensor readings by device and determines stability.
"""

from typing import List, Dict, Any


STABLE_THRESHOLD = 1.0


def group_sensor_readings(
    readings: List[Dict[str, Any]],
    threshold: float = STABLE_THRESHOLD
) -> List[Dict[str, Any]]:
    """
    Groups consecutive sensor readings by device and determines stability.

    Args:
        readings: List of dicts with 'timestamp', 'device_id', 'value'
        threshold: Maximum difference for readings to be considered stable

    Returns:
        List of grouped readings sorted by start_time, each containing:
        - device_id: String identifier
        - readings: List of temperature values
        - start_time: First timestamp in group
        - end_time: Last timestamp in group
        - is_stable: Boolean (True if max - min <= threshold)
    """
    if not readings:
        return []

    groups = []
    current_device = None
    current_group = []

    for reading in readings:
        device_id = reading["device_id"]

        if device_id != current_device:
            if current_group:
                groups.append(_create_group(current_device, current_group, threshold))
            current_device = device_id
            current_group = [reading]
        else:
            current_group.append(reading)

    if current_group:
        groups.append(_create_group(current_device, current_group, threshold))

    groups.sort(key=lambda g: g["start_time"])
    return groups


def _create_group(
    device_id: str,
    readings: List[Dict[str, Any]],
    threshold: float
) -> Dict[str, Any]:
    """Creates a group dict from consecutive readings."""
    values = [r["value"] for r in readings]
    is_stable = (max(values) - min(values)) <= threshold

    return {
        "device_id": device_id,
        "readings": values,
        "start_time": readings[0]["timestamp"],
        "end_time": readings[-1]["timestamp"],
        "is_stable": is_stable
    }


if __name__ == "__main__":
    import json

    test_readings = [
        {"timestamp": 1698000000, "device_id": "sensor_1", "value": 23.5},
        {"timestamp": 1698000005, "device_id": "sensor_1", "value": 23.7},
        {"timestamp": 1698000010, "device_id": "sensor_2", "value": 45.2},
        {"timestamp": 1698000015, "device_id": "sensor_1", "value": 28.1},
        {"timestamp": 1698000055, "device_id": "sensor_1", "value": 31.5},
        {"timestamp": 1698000060, "device_id": "sensor_2", "value": 45.8},
        {"timestamp": 1698000065, "device_id": "sensor_2", "value": 46.1},
    ]

    result = group_sensor_readings(test_readings)
    print(json.dumps(result, indent=2))
