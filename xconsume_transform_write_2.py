""" consume_transform_publish_write_simple.py
    20230715
    After we got a simple write-to-file version working, now working towards mqtt publishing agin

    Consumes the json data from the input file, which is output from rtl_433
    normalizes the data (transform_json_data) and outputs the data:
        - to the console
        - to a file
        - to mqtt
"""
import sys
import time
import json
import logging
import paho.mqtt.client as mqtt
from typing import List, Tuple, Dict
from transform_maps import id_map, model_map
from temp_sensors1 import Sensor_Dev_1 as Sensor

from mqtt_secrets import (
    MQTT_BROKER_ADDRESS,
    MQTT_BROKER_PORT,
    MQTT_USERNAME,
    MQTT_PASSWORD,
)

#
# Configuration Constants
#

OUTPUT_FILE = True
OUTPUT_MQTT = True
OUTPUT_CONSOLE = True

# output file name
FILENAME_OUTPUT = "./Data/sensor_readings.txt"
# FILENAME_OUTPUT = ""

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


# ################# publish data to file and console  #########################


def publish_print(sensor: Sensor) -> None:
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
                file.write(msg)

        publish.last_write_time = current_time  # Update the last write time

    return


# ################# publish data  #########################


def publish(sensor: Sensor) -> None:
    """Publishes the json data to a file"""
    # print(f"### publish: {json_data}")
    sensor_id = sensor.id
    sensor_name = sensor.name
    temperature_F = sensor.temperature_value_f
    humidity = sensor.humidity
    timestamp = f"{sensor.time_date} {sensor.time_time}"

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
                file.write(msg)

        publish.last_write_time = current_time  # Update the last write time

    return


########## Initialize the last write time ##########
publish.last_write_time = time.time()  # Initialize the last write time


# ################# transform_json_data #########################


def transform_json_data(json_data: Dict[str, str]) -> Sensor:
    """converts model and id to human readable values"""
    transformed_data = json_data.copy()

    id: str = "*NO ID*"
    name: str = "*NO NAME*"
    model: str = ""
    time_raw: str = ""
    time_time: str = ""
    time_date: str = ""
    channel: str = json_data["channel"]
    battery: str = json_data["battery_ok"]
    temperature_raw: str = ""
    temperature_value_f: str = ""
    temperature_value_c: str = ""
    humidity_raw: str = ""
    humidity_value: str = ""
    integrity: str = ""

    # transform (normalize) the id (id seems to be an int, although we
    #   check for string values as well
    if "id" in json_data:
        id = "*BAD ID*"
        name = "*BAD NAME*"
        t_id = json_data["id"]  # temporary id
        if t_id in id_map:
            id_data = id_map[id]
            id = id_data["idx"]  # update with good transformation of ID
            name = id_data["name"]  # update with good transformation of name

    # transform (normalize) the model name
    model = "*NO MODEL*"
    if "model" in json_data:
        model = json_data["model"]
        model = model.upper()
        model = model_map.get(model, "*BAD MODEL*")

    # Check for temperature.
    #   if only in celsius convert to fahrenheit and add both
    #   if only in farhenheit convert to celsius and add both

    temperature_raw = "_no raw_"
    if "temperature_raw" in json_data:
        temperature_raw = json_data["temperature_raw"]

    if "temperature_C" not in json_data and "temperature_F" not in json_data:
        temperature_value_c = "__"
        temperature_value_f = "__"
    elif "temperature_C" not in json_data:
        temperature_value_c, temperature_value_f = convert_temperature(
            json_data["temperature_value_f"], "F"
        )
    elif "temperature_value_f" not in json_data:
        temperature_value_c, temperature_value_f = convert_temperature(
            json_data["temperature_value_c"], "C"
        )

    # Check for humidity
    #   Some sensors don't have humidity

    json_data["humidity"] = "*NO HUMIDITY*"
    if "humidity" in json_data:
        humidity = json_data["humidity"]

    dev = Sensor(
        id=id,
        name=name,
        model=model,
        time_raw=time_raw,
        time_time=time_time,
        time_date=time_date,
        channel=channel,
        battery=battery,
        temperature_raw=temperature_raw,
        temperature_value_f=temperature_value_f,
        temperature_value_c=temperature_value_c,
        humidity_raw=humidity_raw,
        humidity_value=humidity_value,
        integrity=integrity,
    )

    return json_data


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

        sensor = transform_json_data(json_data)
        # print(f"*-* consume_transform_publish: {transformed_data}")

        # Publish the transformed data to MQTT
        publish(sensor)


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
