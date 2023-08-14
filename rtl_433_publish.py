""" rtl_433_publish.py
    working  code 20230718
    Publishes to console and to MQTT with appropriate topics
    Broker is defined in mqtt_secrets.py; tested with test.mosquitto.org
    ** 20230717 - adding better start banner
    ** 20230717 - testing with loop bash script
    ** 20230718 - testing wih Vultr MQTT broker and Vultr Ignition Broker
"""
import sys
import json
import time
import datetime
import logging
from logging.handlers import RotatingFileHandler
import paho.mqtt.client as mqtt
from pprint import pprint
from typing import TextIO, Dict
from temp_sensors import Sensor_Dev_1, SensorReadingStack
from mqtt_secrets import MQTT_BROKER, MQTT_BROKER_ADDRESS, MQTT_BROKER_PORT, MQTT_USERNAME, MQTT_PASSWORD


# ###################################################################### #
#                       constants and environment                        #
# ###################################################################### #



MAX_DATA_STORE_TIME: int = 1800  # Maximum data store time in seconds (30 minutes)
MAX_STACK_SIZE: int = 10  # Maximum size of history stacks

PUBLISH_WAIT_TIME_S: int = 60  # Time between publishing to MQTT broker
PUBLISH_TO_CONSOLE: bool = True
PUBLISH_TO_FILE_TEXT: bool = False
PUBLISH_TO_FILE_JSON: bool = False
PUBLISH_TO_MQTT: bool = True


DEFAULT_LOGGING_LEVEL = logging.DEBUG
DEFAULT_LOGFILE_PATH = "/home/karl/Logs"
DEFAULT_LOGFILE_FILENAME = "rtl_433_publish.log"
DEFAULT_LOGFILE_FILESPECT = f"{DEFAULT_LOGFILE_PATH}/{DEFAULT_LOGFILE_FILENAME}"
MAX_LOGFILE_SIZE = 10*1024*1024

# ######################### setup logger  #########################

log_file = DEFAULT_LOGFILE_FILESPECT

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(DEFAULT_LOGGING_LEVEL)  

# Create a rotating file handler which rotates log files
handler = RotatingFileHandler(log_file, maxBytes=MAX_LOGFILE_SIZE, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handler to logger
logger.addHandler(handler)

# ######################### Print Startup Info  #########################


def print_startup_info() -> None:
    BORDER_SIZE: int = 80

    msg = (
        "\n" + "*" * BORDER_SIZE + "\n" +
        f"PUBLISHING TO CONSOLE: {PUBLISH_TO_CONSOLE}\n"
        f"PUBLISHING TO FILE (TEXT): {PUBLISH_TO_FILE_TEXT}\n"
        f"PUBLISHING TO FILE (JSON): {PUBLISH_TO_FILE_JSON}\n"
        f"PUBLISHING TO MQTT: {PUBLISH_TO_MQTT}\n"
    )

    logger.info(msg)


    if PUBLISH_TO_MQTT:
        msg = (
            f"---------------- Single MQTT Broker ----------------\n"
            f"PUBLISH_WAIT_TIME_S: {PUBLISH_WAIT_TIME_S}\n"
            f"PUBLISH_TO_CONSOLE: {PUBLISH_TO_CONSOLE}\n"
            f"PUBLISH_TO_FILE_TEXT: {PUBLISH_TO_FILE_TEXT}\n"
            f"PUBLISH_TO_FILE_JSON: {PUBLISH_TO_FILE_JSON}\n"
            f"PUBLISH_TO_MQTT: {PUBLISH_TO_MQTT}"
        )
        logger.info(msg)

    msg = ("\n" + "*" * BORDER_SIZE + "\n" )
    logger.info(msg)
    return


# ######################### trim a specific stack  #########################


def trim_stack(sensor_stack: SensorReadingStack) -> None:
    format_str = "%Y-%m-%d %H:%M:%S.%f"
    current_time: float = time.time()

    # Iterate over the stack and remove readings older than MAX_DATA_STORE_TIME
    while not sensor_stack.is_empty():
        oldest_reading_time_str: str = sensor_stack.peek().time_raw

        try:
            oldest_reading_time = datetime.datetime.strptime(oldest_reading_time_str, format_str).timestamp()
        except ValueError:
            # If parsing with milliseconds fails, try without milliseconds
            format_str = "%Y-%m-%d %H:%M:%S"
            oldest_reading_time = datetime.datetime.strptime(oldest_reading_time_str, format_str).timestamp()

        if current_time - oldest_reading_time > MAX_DATA_STORE_TIME:
            sensor_stack.pop()
        else:
            break


# ######################### trim all stacks  #########################


def trim_all_stacks(sensor_stacks: Dict[str, SensorReadingStack]) -> None:
    # Iterate over all the sensor stacks and call trim_stack for each stack
    for stack in sensor_stacks.values():
        trim_stack(stack)


# ######################### publish to file  #########################


def publish_to_file(sensor_reading: Sensor_Dev_1) -> None:
    logger.error("Not publishing to file yet")
    return


# ######################### publish to file as json #########################


def publish_to_file_as_json(sensor_reading: Sensor_Dev_1) -> None:
    logger.error("Not publishing to file as json yet")
    return


# ######################### publish to MQTT  #########################


# ######################### publish to a single broker  #########################


def publish_to_broker(
    br_ip: str,
    br_port: int,
    br_user: str,
    br_pass: str,
    topic: str,
    payload: str,
) -> None:
    """does the actual publishing to a single mqtt broker"""

    logger.info(f"Publishing to: {br_ip}, topic: {topic}, \n  {payload}\n")
    client = mqtt.Client()

    # Set MQTT broker credentials
    client.username_pw_set(br_user, br_pass)

    # Connect to MQTT broker
    client.connect(br_ip, br_port)

    # Publish the payload to a specific MQTT topic
    client.publish(topic, payload)

    # Disconnect from MQTT broker
    client.disconnect()
    return


# ######################### publish to all the  brokers  #########################


def publish_to_brokers(sensor_reading: Sensor_Dev_1) -> None:
    """Function to publish the sensor reading to all active MQTT brokers"""

    # Get the topic leaf name
    topic_leaf_name: str = sensor_reading.sensor_name
    topic = f"KTBMES/sensor/readings/{topic_leaf_name}"

    # Prepare the payload
    payload = json.dumps(sensor_reading.to_dict())

    publish_to_broker(
        br_ip=MQTT_BROKER_ADDRESS,
        br_port=MQTT_BROKER_PORT,
        br_user=MQTT_USERNAME,
        br_pass=MQTT_PASSWORD,
        topic=topic,
        payload=payload,
    )

    return


# ######################### publish to console  #########################


def publish_to_console(sensor_reading: Sensor_Dev_1) -> None:
    # Function to publish the sensor reading to the console
    logger.info(sensor_reading)


# ######################### publish data #########################


def publish_data(sensor_stacks: Dict[str, SensorReadingStack]) -> None:
    # Function to publish the data in the sensor stacks based on configuration constants
    logger.debug("+++ Publishing Stacks")

    for stack in sensor_stacks.values():
        if not stack.is_empty():
            recent_reading: Sensor_Dev_1 = stack.peek()
            logger.debug(f"\tid: {recent_reading.id_raw} Name: {recent_reading.sensor_name}")

            if PUBLISH_TO_CONSOLE:
                publish_to_console(recent_reading)

            if PUBLISH_TO_FILE_TEXT:
                publish_to_file(recent_reading)

            if PUBLISH_TO_FILE_JSON:
                publish_to_file_as_json(recent_reading)

            if PUBLISH_TO_MQTT:
                publish_to_brokers(recent_reading)


# ######################### consume - store - publish  #########################

#! Have the Sensor_Dev_1.from_json check for valid keys

def consume_store_publish(file: TextIO) -> None:
    sensor_stacks: Dict[str, SensorReadingStack] = {}
    last_publish_time: float = time.time()

    print_startup_info()

    for line in file:
        line = line.strip()

        if line:
            sensor_reading: Sensor_Dev_1 = Sensor_Dev_1.from_json(line)
            logger.debug(f"*** Reading sensor:\n{sensor_reading}")
            sensor_id = sensor_reading.id_raw

            #! a check for non temp sensors should be made here
            if sensor_reading.id_raw == "":
                logger.info("---- ignoring device")
                continue # for now, we ignore the line

            if sensor_id not in sensor_stacks:
                sensor_stacks[sensor_id] = SensorReadingStack(MAX_STACK_SIZE)

            sensor_stack: SensorReadingStack = sensor_stacks[sensor_id]
            sensor_stack.push(sensor_reading)

        current_time: float = time.time()
        if current_time - last_publish_time >= PUBLISH_WAIT_TIME_S:
            publish_data(sensor_stacks)
            last_publish_time = current_time
            logger.debug("  Trimming stacks")
            trim_all_stacks(sensor_stacks)


# ######################### setup logging  #########################

def setup_logging(log_level=DEFAULT_LOGGING_LEVEL):
    logger = logging.getLogger()
    logger.setLevel(log_level)

    log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(log_format)
    logger.addHandler(stream_handler)

    # You can add more handlers here if needed. For instance, to log to a file.
    # file_handler = logging.handlers.RotatingFileHandler("app.log", maxBytes=1e6, backupCount=5)
    # file_handler.setFormatter(log_format)
    # logger.addHandler(file_handler)


# ######################### Main #########################


def main() -> None:
    setup_logging(DEFAULT_LOGGING_LEVEL)  # Set up logging first with your default logging level
    consume_store_publish(sys.stdin)


if __name__ == "__main__":
    main()
    exit(0)
