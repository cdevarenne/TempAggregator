"""
Async Sensor Stream Processor

Processes multiple sensor streams concurrently with error handling,
retry logic, and batching for high-volume scenarios.
"""

import asyncio
import time
from typing import AsyncGenerator, List, Dict, Any
from collections import deque


MAX_RETRIES = 3
RETRY_BACKOFF_BASE = 0.5
BATCH_SIZE = 10
BATCH_TIMEOUT = 1.0


async def sensor_stream(device_id: str, delay: float) -> AsyncGenerator[Dict[str, Any], None]:
    """Simulates a sensor that produces readings every 'delay' seconds."""
    for i in range(5):
        await asyncio.sleep(delay)
        yield {
            "timestamp": int(time.time()),
            "device_id": device_id,
            "value": 20.0 + (i * 0.5)
        }


async def process_sensor_streams(streams: List[AsyncGenerator]) -> None:
    """
    Process multiple sensor streams concurrently.
    For each reading, print: "device_id: value=X.X"

    Args:
        streams: List of async generators (sensor streams)
    """
    tasks = [_process_single_stream(stream) for stream in streams]
    await asyncio.gather(*tasks)


async def _process_single_stream(stream: AsyncGenerator) -> None:
    """Process a single sensor stream with retry logic."""
    retry_count = 0

    try:
        async for reading in stream:
            success = await _process_reading_with_retry(reading, retry_count)
            if not success:
                retry_count += 1
            else:
                retry_count = 0
    except Exception as e:
        print(f"Error processing stream: {e}")


async def _process_reading_with_retry(reading: Dict[str, Any], retry_count: int) -> bool:
    """Process a single reading with exponential backoff on failure."""
    for attempt in range(MAX_RETRIES):
        try:
            _print_reading(reading)
            return True
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                backoff = RETRY_BACKOFF_BASE * (2 ** attempt)
                await asyncio.sleep(backoff)
            else:
                print(f"Failed to process reading after {MAX_RETRIES} attempts: {e}")
                return False
    return False


def _print_reading(reading: Dict[str, Any]) -> None:
    """Print a single reading in the required format."""
    print(f"{reading['device_id']}: value={reading['value']:.1f}")


async def process_sensor_streams_batched(
    streams: List[AsyncGenerator],
    batch_size: int = BATCH_SIZE,
    batch_timeout: float = BATCH_TIMEOUT
) -> None:
    """
    Process multiple sensor streams with batching for high-volume scenarios.

    Args:
        streams: List of async generators
        batch_size: Maximum batch size before processing
        batch_timeout: Maximum time to wait before processing partial batch
    """
    queue = asyncio.Queue()

    async def collector(stream: AsyncGenerator) -> None:
        """Collect readings from a stream and put in queue."""
        async for reading in stream:
            await queue.put(reading)

    collectors = [asyncio.create_task(collector(stream)) for stream in streams]

    batch = []
    last_process_time = time.time()

    while True:
        try:
            reading = await asyncio.wait_for(queue.get(), timeout=0.1)
            batch.append(reading)

            current_time = time.time()
            should_process = (
                len(batch) >= batch_size or
                current_time - last_process_time >= batch_timeout
            )

            if should_process:
                for r in batch:
                    _print_reading(r)
                batch = []
                last_process_time = current_time

        except asyncio.TimeoutError:
            if all(task.done() for task in collectors):
                if batch:
                    for r in batch:
                        _print_reading(r)
                break

    await asyncio.gather(*collectors)


async def main() -> None:
    """Test concurrent stream processing."""
    streams = [
        sensor_stream("sensor_1", 0.3),
        sensor_stream("sensor_2", 0.5),
        sensor_stream("sensor_3", 0.4),
    ]
    await process_sensor_streams(streams)


if __name__ == "__main__":
    asyncio.run(main())
