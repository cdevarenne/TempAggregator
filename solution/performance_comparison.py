"""
Performance Comparison: Lab1 (Sync) vs Lab2 (Async)

Compares performance characteristics of synchronous grouping
vs asynchronous stream processing.
"""

import time
import asyncio
from typing import List, Dict, Any
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lab1'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lab2'))

from sensor_aggregator import group_sensor_readings
from async_sensor_processor import process_sensor_streams


def generate_test_data(num_devices: int, readings_per_device: int) -> List[Dict[str, Any]]:
    """Generate test data with specified number of devices and readings."""
    readings = []
    timestamp = 1698000000

    for device_idx in range(num_devices):
        device_id = f"sensor_{device_idx + 1}"
        for reading_idx in range(readings_per_device):
            readings.append({
                "timestamp": timestamp,
                "device_id": device_id,
                "value": 20.0 + (reading_idx * 0.5)
            })
            timestamp += 5

    return readings


def benchmark_sync_processing(data: List[Dict[str, Any]]) -> float:
    """Benchmark synchronous grouping (Lab1)."""
    start = time.perf_counter()
    result = group_sensor_readings(data)
    end = time.perf_counter()
    return end - start


async def async_stream_from_data(data: List[Dict[str, Any]], delay: float = 0.001):
    """Convert static data to async stream."""
    for reading in data:
        await asyncio.sleep(delay)
        yield reading


async def benchmark_async_processing(
    data_sets: List[List[Dict[str, Any]]],
    delay: float = 0.001
) -> float:
    """Benchmark async stream processing (Lab2)."""
    start = time.perf_counter()

    streams = [async_stream_from_data(data, delay) for data in data_sets]

    original_print = print
    def silent_print(*args, **kwargs):
        pass

    import builtins
    builtins.print = silent_print

    try:
        await process_sensor_streams(streams)
    finally:
        builtins.print = original_print

    end = time.perf_counter()
    return end - start


def run_benchmarks():
    """Run comprehensive benchmarks."""
    print("=" * 60)
    print("Performance Comparison: Lab1 (Sync) vs Lab2 (Async)")
    print("=" * 60)
    print()

    test_scenarios = [
        ("Small Dataset", 3, 10),
        ("Medium Dataset", 10, 100),
        ("Large Dataset", 20, 500),
    ]

    for scenario_name, num_devices, readings_per_device in test_scenarios:
        print(f"\n{scenario_name}:")
        print(f"  Devices: {num_devices}")
        print(f"  Readings per device: {readings_per_device}")
        print(f"  Total readings: {num_devices * readings_per_device}")

        data = generate_test_data(num_devices, readings_per_device)

        sync_time = benchmark_sync_processing(data)
        print(f"\n  Lab1 (Sync Grouping):")
        print(f"    Execution time: {sync_time:.4f}s")
        print(f"    Throughput: {len(data) / sync_time:.0f} readings/s")

        data_sets = []
        for device_idx in range(num_devices):
            device_data = [r for r in data if r["device_id"] == f"sensor_{device_idx + 1}"]
            data_sets.append(device_data)

        async_time = asyncio.run(benchmark_async_processing(data_sets, delay=0.0001))
        print(f"\n  Lab2 (Async Streaming):")
        print(f"    Execution time: {async_time:.4f}s")
        print(f"    Throughput: {len(data) / async_time:.0f} readings/s")

        speedup = sync_time / async_time if async_time > 0 else 0
        print(f"\n  Speedup: {speedup:.2f}x")
        print("  " + "-" * 56)

    print("\n" + "=" * 60)
    print("\nMemory Characteristics:")
    print("=" * 60)

    print("\nLab1 (Sync Grouping):")
    print("  - Requires all data in memory upfront")
    print("  - Processes entire dataset before returning")
    print("  - O(n) space complexity where n = total readings")
    print("  - Best for: Batch processing of complete datasets")

    print("\nLab2 (Async Streaming):")
    print("  - Processes data as it arrives")
    print("  - Can start outputting before all data received")
    print("  - O(c) space where c = concurrent streams")
    print("  - Best for: Real-time streaming data")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    run_benchmarks()
