import sys
import json
import time
from typing import TextIO, Dict
from temp_sensors2 import Sensor_Dev_1, SensorReadingStack

MAX_STACK_SIZE: int = 10
PUBLISH_WAIT_TIME_S: int = 60


# ######################### publish to console  #########################


def publish_to_console(sensor_reading: Sensor_Dev_1) -> None:
    # Function to publish the sensor reading to the console
    print(sensor_reading)


# ######################### publish data #########################


def publish_data(sensor_stacks: Dict[str, SensorReadingStack]) -> None:
    # Function to publish the data in the sensor stacks
    for stack in sensor_stacks.values():
        if not stack.is_empty():
            recent_reading: Sensor_Dev_1 = stack.peek()
            publish_to_console(recent_reading)


# ######################### consume - store - publish  #########################


def consume_store_publish(file: TextIO) -> None:
    sensor_stacks: Dict[str, SensorReadingStack] = {}
    last_publish_time: float = time.time()

    for line in file:
        line = line.strip()

        if line:
            sensor_reading: Sensor_Dev_1 = Sensor_Dev_1.from_json(line)

            sensor_id: str = sensor_reading.id_raw
            if sensor_id not in sensor_stacks:
                sensor_stacks[sensor_id] = SensorReadingStack(MAX_STACK_SIZE)
            sensor_stack: SensorReadingStack = sensor_stacks[sensor_id]
            sensor_stack.push(sensor_reading)

        current_time: float = time.time()
        if current_time - last_publish_time >= PUBLISH_WAIT_TIME_S:
            publish_data(sensor_stacks)
            last_publish_time = current_time


# ######################### Main #########################


def main() -> None:
    consume_store_publish(sys.stdin)


if __name__ == "__main__":
    main()
    exit(0)
