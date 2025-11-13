"""
Sensor Reading Aggregator - Interview Exercise

Your task: Implement the function below to group sensor readings by device
and determine if each group is stable.

Run with: python3 sensor_aggregator.py
"""


def group_sensor_readings(readings):
    """
    Groups consecutive sensor readings by device and determines stability.

    Args:
        readings: List of dicts with 'timestamp', 'device_id', 'value'

    Returns:
        List of grouped readings with stability info.
        Each group should have:
        - device_id: String
        - readings: List of values
        - start_time: First timestamp in group
        - end_time: Last timestamp in group
        - is_stable: Boolean (True if all values within ±1.0 degrees)
    """
    # TODO: Implement this function
    pass


# Test data
if __name__ == "__main__":
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

    # Pretty print the result
    import json
    print(json.dumps(result, indent=2))


