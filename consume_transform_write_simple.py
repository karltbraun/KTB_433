""" consume_transform_publish_write_simple.py
    20230714
    Consumes the json data from the input file, which is output from rtl_433
    normalizes the data (transform_json_data) and writes it to a file
    Presumably the file is consumed by either a web page or other display mechanism
"""
import sys
import json
import logging
import paho.mqtt.client as mqtt
from typing import List
from transform_maps import id_map, model_map

"""
from mqtt_secrets import (
    MQTT_BROKER_ADDRESS,
    MQTT_BROKER_PORT,
    MQTT_USERNAME,
    MQTT_PASSWORD,
)
"""

#
# Configuration Constants
#

# output file name
FILENAME_OUTPUT = "sensor_readings.txt"

# LOG FILE CONFIGURATION
LOGFILE_PATH = "/var/log"
LOGFILE_DIR = "rtl_433_simple"
LOGFILE_FILENAME = f"{LOGFILE_PATH}/{LOGFILE_DIR}/rtl_433_simple.log"

LOG_LEVEL = logging.DEBUG
LOGFILE_MAX_BYTES = 2048
LOGFILE_BACKUP_COUNT = 5

#
# output dictionary and list
#

dct_sensor_1 = {
    "id": "",
    "name": "",
    "temp_f": "",
    "humidity": "",
    "date": "",
    "time": "",
}
lst_sensor_readings: List[dct_sensor_1] = []

#
# Set up global logging
#

logger = logging.getLogger()
log_handler = logging.handlers.RotatingFileHandler(
    LOGFILE_FILENAME, maxBytes=LOGFILE_MAX_BYTES, backupCount=LOGFILE_BACKUP_COUNT
)
log_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(log_handler)
logger.setLevel(LOG_LEVEL)


# ################# publish data  #########################


def publish(json_data):
    """Publishes the json data to a file"""

    id = json_data["id"]
    name = json_data["name"]
    temp_f = json_data["temp_f"]
    humidity = json_data["humidity"]
    timestamp = f"{json_data['date']} {json_data['time']}"

    msg = (
        f"Sensor: {id:<5} - {name:<10}\n"
        f"  Timestamp: {timestamp}\n"
        f"  Temp: {temp_f:<5}F\n"
        f"  Humidity: {humidity:<5}%\n"
    )

    with open(FILENAME_OUTPUT, "w") as f:
        f.write(msg)

    return


# ################# transform_json_data #########################


def transform_json_data(json_data):
    """converts model and id to human readable values"""
    transformed_data = json_data.copy()

    if "model" in transformed_data:
        transformed_data["model"] = model_map.get(
            transformed_data["model"], transformed_data["model"]
        )

    if "id" in transformed_data:
        transformed_data["id"] = id_map.get(
            transformed_data["id"], transformed_data["id"]
        )

    return transformed_data


# ################# consume_transform_publish  #########################


def consume_transform_publish(file):
    """Consumes the json data from the input file,
    normalizes the data (transform_json_data) and publishes it to MQTT)
    """
    for line in file:
        logger.debug(f"Processing: {json_data}")

        try:
            json_data = json.loads(line)
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON data - {line.strip()}")

        # check for known model

        if "model" not in json_data:
            logger.warning(
                f"WARNING: No model in JSON data, skipping entry\n  {json_data}"
            )
            continue

        if json_data["model"] not in model_map:
            logger.warning(
                f"WARNING: Model not in model_map, skipping entry\n  {json_data}"
            )
            continue

        # check for known id

        if "id" not in json_data:
            logger.warning(
                f"WARNING: No id in JSON data, skipping entry\n  {json_data}"
            )
            continue

        if json_data["id"] not in id_map:
            logger.warning(
                f"WARNING: id not in id_map, continuing with unknown id\n  {json_data}"
            )

        transformed_data = transform_json_data(json_data)

        # Publish the transformed data to MQTT
        publish(transformed_data)


# ################# MAIN #########################


def main():
    """Define input file a standard input and call consume_transform_publish"""

    # Define the input file
    input_file = sys.stdin

    # now do the bulk of the work
    consume_transform_publish(input_file)


if __name__ == "__main__":
    main()
