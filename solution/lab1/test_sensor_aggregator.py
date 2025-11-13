"""
Tests for Sensor Reading Aggregator
"""

import unittest
from sensor_aggregator import group_sensor_readings


class TestGroupSensorReadings(unittest.TestCase):
    """Test cases for group_sensor_readings function."""

    def test_basic_grouping(self):
        """Test basic consecutive grouping by device."""
        readings = [
            {"timestamp": 1698000000, "device_id": "sensor_1", "value": 23.5},
            {"timestamp": 1698000005, "device_id": "sensor_1", "value": 23.7},
            {"timestamp": 1698000010, "device_id": "sensor_2", "value": 45.2},
            {"timestamp": 1698000015, "device_id": "sensor_1", "value": 28.1},
            {"timestamp": 1698000055, "device_id": "sensor_1", "value": 31.5},
            {"timestamp": 1698000060, "device_id": "sensor_2", "value": 45.8},
            {"timestamp": 1698000065, "device_id": "sensor_2", "value": 46.1},
        ]

        result = group_sensor_readings(readings)

        self.assertEqual(len(result), 4)

        self.assertEqual(result[0]["device_id"], "sensor_1")
        self.assertEqual(result[0]["readings"], [23.5, 23.7])
        self.assertEqual(result[0]["start_time"], 1698000000)
        self.assertEqual(result[0]["end_time"], 1698000005)
        self.assertTrue(result[0]["is_stable"])

        self.assertEqual(result[1]["device_id"], "sensor_2")
        self.assertEqual(result[1]["readings"], [45.2])
        self.assertTrue(result[1]["is_stable"])

        self.assertEqual(result[2]["device_id"], "sensor_1")
        self.assertEqual(result[2]["readings"], [28.1, 31.5])
        self.assertFalse(result[2]["is_stable"])

        self.assertEqual(result[3]["device_id"], "sensor_2")
        self.assertEqual(result[3]["readings"], [45.8, 46.1])
        self.assertTrue(result[3]["is_stable"])

    def test_empty_input(self):
        """Test with empty input list."""
        result = group_sensor_readings([])
        self.assertEqual(result, [])

    def test_single_reading(self):
        """Test with single reading."""
        readings = [{"timestamp": 1698000000, "device_id": "sensor_1", "value": 23.5}]
        result = group_sensor_readings(readings)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["device_id"], "sensor_1")
        self.assertEqual(result[0]["readings"], [23.5])
        self.assertTrue(result[0]["is_stable"])

    def test_all_same_device(self):
        """Test with all readings from same device."""
        readings = [
            {"timestamp": 1698000000, "device_id": "sensor_1", "value": 23.5},
            {"timestamp": 1698000005, "device_id": "sensor_1", "value": 24.0},
            {"timestamp": 1698000010, "device_id": "sensor_1", "value": 24.5},
        ]
        result = group_sensor_readings(readings)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["device_id"], "sensor_1")
        self.assertEqual(result[0]["readings"], [23.5, 24.0, 24.5])
        self.assertTrue(result[0]["is_stable"])

    def test_stability_threshold_exact(self):
        """Test stability at exact threshold boundary."""
        readings = [
            {"timestamp": 1698000000, "device_id": "sensor_1", "value": 20.0},
            {"timestamp": 1698000005, "device_id": "sensor_1", "value": 21.0},
        ]
        result = group_sensor_readings(readings)

        self.assertTrue(result[0]["is_stable"])

        readings = [
            {"timestamp": 1698000000, "device_id": "sensor_1", "value": 20.0},
            {"timestamp": 1698000005, "device_id": "sensor_1", "value": 21.1},
        ]
        result = group_sensor_readings(readings)

        self.assertFalse(result[0]["is_stable"])

    def test_custom_threshold(self):
        """Test with custom stability threshold."""
        readings = [
            {"timestamp": 1698000000, "device_id": "sensor_1", "value": 20.0},
            {"timestamp": 1698000005, "device_id": "sensor_1", "value": 22.5},
        ]

        result_default = group_sensor_readings(readings)
        self.assertFalse(result_default[0]["is_stable"])

        result_custom = group_sensor_readings(readings, threshold=3.0)
        self.assertTrue(result_custom[0]["is_stable"])

    def test_unsorted_input_by_start_time(self):
        """Test that output is sorted by start_time chronologically."""
        readings = [
            {"timestamp": 1698000060, "device_id": "sensor_2", "value": 45.8},
            {"timestamp": 1698000065, "device_id": "sensor_2", "value": 46.1},
            {"timestamp": 1698000000, "device_id": "sensor_1", "value": 23.5},
            {"timestamp": 1698000005, "device_id": "sensor_1", "value": 23.7},
        ]
        result = group_sensor_readings(readings)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["start_time"], 1698000000)
        self.assertEqual(result[1]["start_time"], 1698000060)

    def test_multiple_device_switches(self):
        """Test with multiple device switches."""
        readings = [
            {"timestamp": 1698000000, "device_id": "sensor_1", "value": 20.0},
            {"timestamp": 1698000005, "device_id": "sensor_2", "value": 30.0},
            {"timestamp": 1698000010, "device_id": "sensor_1", "value": 21.0},
            {"timestamp": 1698000015, "device_id": "sensor_2", "value": 31.0},
        ]
        result = group_sensor_readings(readings)

        self.assertEqual(len(result), 4)
        self.assertEqual(result[0]["device_id"], "sensor_1")
        self.assertEqual(result[1]["device_id"], "sensor_2")
        self.assertEqual(result[2]["device_id"], "sensor_1")
        self.assertEqual(result[3]["device_id"], "sensor_2")

    def test_large_value_range(self):
        """Test with large temperature variation."""
        readings = [
            {"timestamp": 1698000000, "device_id": "sensor_1", "value": 10.0},
            {"timestamp": 1698000005, "device_id": "sensor_1", "value": 50.0},
        ]
        result = group_sensor_readings(readings)

        self.assertFalse(result[0]["is_stable"])

    def test_identical_values(self):
        """Test with all identical values."""
        readings = [
            {"timestamp": 1698000000, "device_id": "sensor_1", "value": 23.5},
            {"timestamp": 1698000005, "device_id": "sensor_1", "value": 23.5},
            {"timestamp": 1698000010, "device_id": "sensor_1", "value": 23.5},
        ]
        result = group_sensor_readings(readings)

        self.assertTrue(result[0]["is_stable"])

    def test_negative_temperatures(self):
        """Test with negative temperature values."""
        readings = [
            {"timestamp": 1698000000, "device_id": "sensor_1", "value": -5.0},
            {"timestamp": 1698000005, "device_id": "sensor_1", "value": -5.5},
        ]
        result = group_sensor_readings(readings)

        self.assertTrue(result[0]["is_stable"])


if __name__ == "__main__":
    unittest.main()
