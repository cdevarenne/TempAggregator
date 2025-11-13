"""
Async Bonus Challenge - Concurrent Sensor Stream Processing

Problem: Process 3 sensor streams concurrently and print readings as they arrive.

Expected output: Readings from different sensors should be interleaved,
demonstrating true concurrent processing.
"""

import asyncio
import time


async def sensor_stream(device_id: str, delay: float):
    """Simulates a sensor that produces readings every 'delay' seconds"""
    for i in range(5):
        await asyncio.sleep(delay)
        yield {
            "timestamp": int(time.time()),
            "device_id": device_id,
            "value": 20.0 + (i * 0.5)  # Gradually increasing temperature
        }


async def process_sensor_streams(streams):
    """
    Process multiple sensor streams concurrently.
    For each reading, print: "device_id: value=X.X"

    Args:
        streams: List of async generators (sensor streams)
    """
    # TODO: Implement concurrent processing
    pass


# Test it
async def main():
    streams = [
        sensor_stream("sensor_1", 0.3),
        sensor_stream("sensor_2", 0.5),
        sensor_stream("sensor_3", 0.4),
    ]
    await process_sensor_streams(streams)


if __name__ == "__main__":
    asyncio.run(main())
