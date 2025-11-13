"""
Tests for Async Sensor Stream Processor
"""

import asyncio
import unittest
from unittest.mock import AsyncMock, patch, MagicMock
from io import StringIO
from async_sensor_processor import (
    process_sensor_streams,
    process_sensor_streams_batched,
    sensor_stream,
    _process_reading_with_retry,
    _print_reading
)


class TestAsyncSensorProcessor(unittest.TestCase):
    """Test cases for async sensor stream processor."""

    def test_sensor_stream_generation(self):
        """Test that sensor stream generates correct readings."""
        async def run_test():
            readings = []
            async for reading in sensor_stream("test_sensor", 0.01):
                readings.append(reading)

            self.assertEqual(len(readings), 5)
            self.assertEqual(readings[0]["device_id"], "test_sensor")
            self.assertEqual(readings[0]["value"], 20.0)
            self.assertEqual(readings[1]["value"], 20.5)
            self.assertEqual(readings[4]["value"], 22.0)

        asyncio.run(run_test())

    def test_concurrent_stream_processing(self):
        """Test concurrent processing of multiple streams."""
        async def run_test():
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                streams = [
                    sensor_stream("sensor_1", 0.01),
                    sensor_stream("sensor_2", 0.01),
                ]
                await process_sensor_streams(streams)

                output = mock_stdout.getvalue()
                self.assertIn("sensor_1:", output)
                self.assertIn("sensor_2:", output)

                lines = output.strip().split("\n")
                self.assertEqual(len(lines), 10)

        asyncio.run(run_test())

    def test_print_reading_format(self):
        """Test reading print format."""
        reading = {"device_id": "sensor_1", "value": 23.456}

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            _print_reading(reading)
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, "sensor_1: value=23.5")

    def test_retry_logic_success(self):
        """Test retry logic succeeds on first attempt."""
        async def run_test():
            reading = {"device_id": "sensor_1", "value": 23.5}

            with patch("sys.stdout", new_callable=StringIO):
                result = await _process_reading_with_retry(reading, 0)
                self.assertTrue(result)

        asyncio.run(run_test())

    def test_interleaved_output(self):
        """Test that streams are processed concurrently with interleaving."""
        async def run_test():
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                streams = [
                    sensor_stream("sensor_1", 0.02),
                    sensor_stream("sensor_2", 0.03),
                    sensor_stream("sensor_3", 0.01),
                ]
                await process_sensor_streams(streams)

                output = mock_stdout.getvalue()
                lines = output.strip().split("\n")

                self.assertEqual(len(lines), 15)

                sensor_1_count = sum(1 for line in lines if "sensor_1" in line)
                sensor_2_count = sum(1 for line in lines if "sensor_2" in line)
                sensor_3_count = sum(1 for line in lines if "sensor_3" in line)

                self.assertEqual(sensor_1_count, 5)
                self.assertEqual(sensor_2_count, 5)
                self.assertEqual(sensor_3_count, 5)

        asyncio.run(run_test())

    def test_empty_stream_list(self):
        """Test with empty stream list."""
        async def run_test():
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                await process_sensor_streams([])
                output = mock_stdout.getvalue()
                self.assertEqual(output, "")

        asyncio.run(run_test())

    def test_single_stream(self):
        """Test with single stream."""
        async def run_test():
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                streams = [sensor_stream("sensor_1", 0.01)]
                await process_sensor_streams(streams)

                output = mock_stdout.getvalue()
                lines = output.strip().split("\n")
                self.assertEqual(len(lines), 5)

        asyncio.run(run_test())

    def test_stream_values_precision(self):
        """Test that values are formatted with correct precision."""
        async def run_test():
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                streams = [sensor_stream("sensor_1", 0.01)]
                await process_sensor_streams(streams)

                output = mock_stdout.getvalue()
                for line in output.strip().split("\n"):
                    self.assertRegex(line, r"sensor_1: value=\d+\.\d")

        asyncio.run(run_test())


class TestBatchedProcessing(unittest.TestCase):
    """Test cases for batched stream processing."""

    def test_batched_processing_small_volume(self):
        """Test batched processing with small volume."""
        async def run_test():
            async def small_stream(device_id: str):
                for i in range(3):
                    await asyncio.sleep(0.01)
                    yield {"device_id": device_id, "value": 20.0 + i}

            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                streams = [small_stream("sensor_1"), small_stream("sensor_2")]
                await process_sensor_streams_batched(streams, batch_size=5, batch_timeout=0.1)

                output = mock_stdout.getvalue()
                lines = output.strip().split("\n")
                self.assertEqual(len(lines), 6)

        asyncio.run(run_test())


if __name__ == "__main__":
    unittest.main()
