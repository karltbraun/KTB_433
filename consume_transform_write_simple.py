""" consume_transform_publish_write_simple.py
    20230714
    Consumes the json data from the input file, which is output from rtl_433
    normalizes the data (transform_json_data) and writes it to a file
    Presumably the file is consumed by either a web page or other display mechanism
"""
import sys
import time
import json
import logging
import paho.mqtt.client as mqtt
from typing import List
from transform_maps import id_map, model_map, name_map

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
# FILENAME_OUTPUT = "sensor_readings.txt"
FILENAME_OUTPUT = ""

# LOG FILE CONFIGURATION
"""
LOGFILE_PATH = "/var/log"
LOGFILE_DIR = "rtl_433_simple"
LOGFILE_FILENAME = f"{LOGFILE_PATH}/{LOGFILE_DIR}/rtl_433_simple.log"

LOG_LEVEL = logging.DEBUG
LOGFILE_MAX_BYTES = 2048
LOGFILE_BACKUP_COUNT = 5
"""

#
# output dictionary and list
#

dct_sensor_data = {}  # Updated name for the dictionary

#
# Set up global logging
#

"""
logger = logging.getLogger()
log_handler = logging.handlers.RotatingFileHandler(
    LOGFILE_FILENAME, maxBytes=LOGFILE_MAX_BYTES, backupCount=LOGFILE_BACKUP_COUNT
)
log_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(log_handler)
logger.setLevel(LOG_LEVEL)
"""


# ################# publish data  #########################


def publish(json_data):
    """Publishes the json data to a file"""
    print(f"### publish: {json_data}")
    sensor_id = json_data["id"]
    temp_f = json_data["temp_f"]
    humidity = json_data["humidity"]
    timestamp = f"{json_data['date']} {json_data['time']}"
    sensor_name = name_map.get(json_data["id"], "****")

    # Check if the sensor already exists in the dictionary
    if sensor_id in dct_sensor_data:
        # Update the existing sensor data
        dct_sensor_data[sensor_id]["data"]["name"] = sensor_name
        dct_sensor_data[sensor_id]["data"]["temp_f"] = temp_f
        dct_sensor_data[sensor_id]["data"]["humidity"] = humidity
        dct_sensor_data[sensor_id]["data"]["timestamp"] = timestamp
    else:
        # Add a new sensor to the dictionary
        dct_sensor_data[sensor_id] = {
            "id": sensor_id,
            "data": {
                "name": sensor_name,
                "temp_f": temp_f,
                "humidity": humidity,
                "timestamp": timestamp,
            },
        }

    # Check if 2 minutes have passed since the last write
    current_time = time.time()
    print(f"publish: time: {current_time}: {json_data}")
    if current_time - publish.last_write_time > 120:  # Check if 2 minutes have passed
        # Write the updated sensor data to a file
        print(f"publish: Time to publsih")
        if FILENAME_OUTPUT == "":
            for sensor_id, sensor_info in dct_sensor_data.items():
                json_data = json.dumps(sensor_info["data"])
                print(f"{sensor_id}: {json_data}\n")
        else:
            with open(FILENAME_OUTPUT, "w") as file:
                for sensor_id, sensor_info in dct_sensor_data.items():
                    json_data = json.dumps(sensor_info["data"])
                    file.write(f"{sensor_id}: {json_data}\n")

        publish.last_write_time = current_time  # Update the last write time

    return


########## Initialize the last write time ##########
publish.last_write_time = time.time()  # Initialize the last write time


# ################# transform_json_data #########################


def transform_json_data(json_data):
    """converts model and id to human readable values"""
    transformed_data = json_data.copy()

    if "model" in transformed_data:
        model = transformed_data["model"]
        model = model.upper()
        transformed_data["model"] = model_map.get(model, "*BAD MODEL*")

    if "id" in transformed_data:
        id = transformed_data["id"]
        transformed_data["id"] = id_map.get(transformed_data["id"], "*BAD ID*")

    return transformed_data


# ################# consume_transform_publish  #########################


def consume_transform_publish(file):
    """Consumes the json data from the input file,
    normalizes the data (transform_json_data) and publishes it to MQTT)
    """
    for line in file:
        # logger.debug(f"Processing: {json_data}")

        try:
            json_data = json.loads(line)
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON data - {line.strip()}")

        # print(f"**consume_transform_publish: {json_data}")
        # check for known model

        """
        if "model" not in json_data:
            msg = f"WARNING: No model in JSON data, skipping entry\n  {json_data}"
            # logger.warning(msg)
            print(msg)
            continue

        if json_data["model"] not in model_map:
            msg = f"WARNING: Model not in model_map, skipping entry\n  {json_data}"
            # logger.warning(msg)
            print(msg)
            continue

        # check for known id

        if "id" not in json_data:
            msg = f"WARNING: No id in JSON data, skipping entry\n  {json_data}"
            # logger.warning(msg)
            print(msg)
            continue

        if json_data["id"] not in id_map:
            msg = (
                f"WARNING: id not in id_map, continuing with unknown id\n  {json_data}"
            )
            # logger.warning(msg)
            print(msg)
            pass
        """

        transformed_data = transform_json_data(json_data)
        print(f"*-* consume_transform_publish: {transformed_data}")

        # Publish the transformed data to MQTT
        publish(transformed_data)


# ################# MAIN #########################


def main():
    """Define input file a standard input and call consume_transform_publish"""

    # Define the input file
    input_file = sys.stdin

    # now do the bulk of the work
    print("**Starting consume_transform_publish")
    consume_transform_publish(input_file)


if __name__ == "__main__":
    main()
