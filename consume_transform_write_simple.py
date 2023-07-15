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
from typing import List, Tuple
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
# FILENAME_OUTPUT = "sensor_readings.txt"
FILENAME_OUTPUT = ""

# Publish wait time
#   we don't want to publish every single data collection - not necessary and will fill up files
#   so we update our local data everytime we get a json data packet, but we only publish
#   every PUBLISH_WAIT_SECONDS

# PUBLISH_WAIT_SECONDS = 120
PUBLISH_WAIT_SECONDS = 0

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

# ################# Convert Temperature #####################


def convert_temperature(value: float, unit: str) -> Tuple[float, float]:
    """Given Temperature and Units ('C' or 'F'), return tuple of (Celsius, Fahrenheit)"""
    if unit is None:
        unit = "F"
    unit = unit.upper()

    if unit == "F":
        # Convert Fahrenheit to Celsius
        degrees_f = value
        degrees_c = round((value - 32) * 5 / 9, 2)

    elif unit == "C":
        # Convert Celsius to Fahrenheit
        degrees_c = value
        degrees_f = round((value * 9 / 5) + 32, 2)

    else:
        raise ValueError(f"ERROR: bad temperature unit ({unit})")

    return (degrees_c, degrees_f)


# ################# publish data  #########################


def publish(json_data):
    """Publishes the json data to a file"""
    # print(f"### publish: {json_data}")
    sensor_id = json_data["id"]
    temperature_F = json_data["temperature_F"]
    humidity = json_data["humidity"]
    timestamp = json_data["time"]
    sensor_name = json_data["name"]

    # Check if the sensor already exists in the dictionary
    if sensor_id in dct_sensor_data:
        # Update the existing sensor data
        dct_sensor_data[sensor_id]["data"]["name"] = sensor_name
        dct_sensor_data[sensor_id]["data"]["temperature_F"] = temperature_F
        dct_sensor_data[sensor_id]["data"]["humidity"] = humidity
        dct_sensor_data[sensor_id]["data"]["timestamp"] = timestamp
    else:
        # Add a new sensor to the dictionary
        dct_sensor_data[sensor_id] = {
            "id": sensor_id,
            "data": {
                "name": sensor_name,
                "temperature_F": temperature_F,
                "humidity": humidity,
                "timestamp": timestamp,
            },
        }

    # Check if time to publish
    current_time = time.time()
    # print(f"publish: time: {current_time}: {json_data}")
    if (
        current_time - publish.last_write_time > PUBLISH_WAIT_SECONDS
    ):  # only publish periodically
        # Write the updated sensor data to a file
        print(f"---------- time to publish ----------")

        msg = "\n"
        for sensor_id, sensor_info in dct_sensor_data.items():
            json_data = sensor_info["data"]
            # print(f"json_data: {json_data}")
            id = sensor_id
            timestamp = json_data["timestamp"]
            name = json_data["name"]
            temperature_F = json_data["temperature_F"]
            humidity = json_data["humidity"]
            msg = (
                f"{msg}"
                f"{timestamp:<20} {id:<10} {name:<10} {temperature_F:<10}F, {humidity}%\n"
            )

        print(msg)
        if FILENAME_OUTPUT != "":
            with open(FILENAME_OUTPUT, "w") as file:
                print(msg)

        publish.last_write_time = current_time  # Update the last write time

    return


########## Initialize the last write time ##########
publish.last_write_time = time.time()  # Initialize the last write time


# ################# transform_json_data #########################


def transform_json_data(json_data):
    """converts model and id to human readable values"""
    transformed_data = json_data.copy()

    # transform (normalize) the id (id seems to be an int, although we
    #   check for string values as well
    if "id" in transformed_data:
        id = transformed_data["id"]
        if id in id_map:
            id_data = id_map[id]
            transformed_data["id"] = id_data["idx"]
            transformed_data["name"] = id_data["name"]
        else:
            transformed_data["id"] = "*BAD ID*"
            transformed_data["name"] = "*BAD NAME*"
    else:
        transformed_data["id"] = "*NO ID*"
        transformed_data["name"] = "*NO NAME*"

    # transform (normalize) the model name
    if "model" in transformed_data:
        model = transformed_data["model"]
        model = model.upper()
        transformed_data["model"] = model_map.get(model, "*BAD MODEL*")
    else:
        transformed_data["model"] = "*NO MODEL*"

    # Check for temperature.
    #   if only in celsius convert to fahrenheit and add both
    #   if only in farhenheit convert to celsius and add both

    if (
        "temperature_C" not in transformed_data
        and "temperature_F" not in transformed_data
    ):
        raise ValueError("ERROR: No temperature in JSON data\n--{json_data}")

    if "temperature_C" not in transformed_data:
        temperature_C, temperature_F = convert_temperature(
            transformed_data["temperature_F"], "F"
        )
    elif "temperature_F" not in transformed_data:
        temperature_C, temperature_F = convert_temperature(
            transformed_data["temperature_C"], "C"
        )

    transformed_data["temperature_C"] = temperature_C
    transformed_data["temperature_F"] = temperature_F

    # Check for humidity
    #   Some sensors don't have humidity

    if "humidity" not in transformed_data:
        transformed_data["humidity"] = "*NO HUMIDITY*"

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
        # print(f"*-* consume_transform_publish: {transformed_data}")

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
