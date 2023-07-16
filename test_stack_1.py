import sys
import json
from typing import TextIO, Dict
from temp_sensors2 import Sensor_Dev_1, SensorReadingStack

MAX_STACK_SIZE: int = 10
PUBLISH_INTERVAL: int = 15


# ######################### publish to console  #########################


def publish_to_console(sensor_reading: Sensor_Dev_1) -> None:
    # Function to publish the sensor reading to the console
    print(sensor_reading)


# ######################### consume - store - publish  #########################


def consume_store_publish(file: TextIO) -> None:
    sensor_stacks: Dict[str, SensorReadingStack] = {}
    iteration: int = 0

    for line in file:
        line = line.strip()

        if line:
            sensor_reading: Sensor_Dev_1 = Sensor_Dev_1.from_json(line)

            sensor_id: str = sensor_reading.id_raw
            if sensor_id not in sensor_stacks:
                sensor_stacks[sensor_id] = SensorReadingStack(MAX_STACK_SIZE)
            sensor_stack: SensorReadingStack = sensor_stacks[sensor_id]
            sensor_stack.push(sensor_reading)

            if iteration % PUBLISH_INTERVAL == 0:
                for stack in sensor_stacks.values():
                    if not stack.is_empty():
                        recent_reading: Sensor_Dev_1 = stack.peek()
                        publish_to_console(recent_reading)

        iteration += 1


# ######################### Main #########################


def main() -> None:
    consume_store_publish(sys.stdin)


if __name__ == "__main__":
    main()
    exit(0)
