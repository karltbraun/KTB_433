""" test_stack_1.py
    Working code 20230717
    Publishes to console and to MQTT with appropriate topics
    Broker is defined in mqtt_secrets.py; tested with test.mosquitto.org
"""
import sys
import json
import time
import paho.mqtt.client as mqtt
from typing import TextIO, Dict
from temp_sensors import Sensor_Dev_1, SensorReadingStack
from mqtt_secrets import (
    MQTT_BROKER_ADDRESS,
    MQTT_BROKER_PORT,
    MQTT_USERNAME,
    MQTT_PASSWORD,
)

MAX_STACK_SIZE: int = 10
PUBLISH_WAIT_TIME_S: int = 60
PUBLISH_TO_CONSOLE: bool = True
PUBLISH_TO_FILE_TEXT: bool = False
PUBLISH_TO_FILE_JSON: bool = False
PUBLISH_TO_MQTT: bool = True


# ######################### publish to file  #########################


def publish_to_file(sensor_reading: Sensor_Dev_1) -> None:
    print("Not publishing to file yet")
    return


# ######################### publish to file as json #########################


def publish_to_file_as_json(sensor_reading: Sensor_Dev_1) -> None:
    print("Not publishing to file as json yet")
    return


# ######################### publish to MQTT  #########################


def publish_to_mqtt(sensor_reading: Sensor_Dev_1) -> None:
    # Function to publish the sensor reading to an MQTT broker

    # Get the topic leaf name
    topic_leaf_name: str = sensor_reading.sensor_name
    topic = f"KTBMES/sensor/readings/{topic_leaf_name}"

    client = mqtt.Client()

    # Set MQTT broker credentials
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

    # Connect to MQTT broker
    client.connect(MQTT_BROKER_ADDRESS, MQTT_BROKER_PORT)

    # Prepare the payload
    payload = json.dumps(sensor_reading.to_dict())

    # Publish the payload to a specific MQTT topic
    client.publish(topic, payload)

    # Disconnect from MQTT broker
    client.disconnect()


# ######################### publish to console  #########################


def publish_to_console(sensor_reading: Sensor_Dev_1) -> None:
    # Function to publish the sensor reading to the console
    print(sensor_reading)


# ######################### publish data #########################


def publish_data(sensor_stacks: Dict[str, SensorReadingStack]) -> None:
    # Function to publish the data in the sensor stacks based on configuration constants
    for stack in sensor_stacks.values():
        if not stack.is_empty():
            recent_reading: Sensor_Dev_1 = stack.peek()

            if PUBLISH_TO_CONSOLE:
                publish_to_console(recent_reading)

            if PUBLISH_TO_FILE_TEXT:
                publish_to_file(recent_reading)

            if PUBLISH_TO_FILE_JSON:
                publish_to_file_as_json(recent_reading)

            if PUBLISH_TO_MQTT:
                publish_to_mqtt(recent_reading)


# ######################### consume - store - publish  #########################


def consume_store_publish(file: TextIO) -> None:
    sensor_stacks: Dict[str, SensorReadingStack] = {}
    last_publish_time: float = time.time()

    msg = (
        f"PUBLISHING TO CONSOLE: {PUBLISH_TO_CONSOLE}\n"
        f"PUBLISHING TO FILE (TEXT): {PUBLISH_TO_FILE_TEXT}\n"
        f"PUBLISHING TO FILE (JSON): {PUBLISH_TO_FILE_JSON}\n"
        f"PUBLISHING TO MQTT: {PUBLISH_TO_MQTT}\n"
    )
    print(msg)

    if PUBLISH_TO_MQTT:
        msg = (
            f"MQTT BROKER ADDRESS: {MQTT_BROKER_ADDRESS}\n"
            f"MQTT BROKER PORT: {MQTT_BROKER_PORT}\n"
            f"MQTT USERNAME: {MQTT_USERNAME}\n"
            f"MQTT PASSWORD: {MQTT_PASSWORD}\n"
            "\n"
            f"PUBLISH_WAIT_TIME_S: {PUBLISH_WAIT_TIME_S}\n"
            f"PUBLISH_TO_CONSOLE: {PUBLISH_TO_CONSOLE}\n"
            f"PUBLISH_TO_FILE_TEXT: {PUBLISH_TO_FILE_TEXT}\n"
            f"PUBLISH_TO_FILE_JSON: {PUBLISH_TO_FILE_JSON}\n"
            f"PUBLISH_TO_MQTT: {PUBLISH_TO_MQTT}"
        )
        print(msg)

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
