""" consume_transform_publish
    working script as of 20230713
    Consumes the json data from the input file, which is output from rtl_433
    normalizes the data (transform_json_data) and publishes it to MQTT)
"""
import sys
import json
import logging
import paho.mqtt.client as mqtt
from transform_maps import id_map, model_map
from mqtt_secrets import (
    MQTT_BROKER_ADDRESS,
    MQTT_BROKER_PORT,
    MQTT_USERNAME,
    MQTT_PASSWORD,
)

#
# Configuration Constants
#

# LOG FILE CONFIGURATION
LOGFILE_PATH = "/var/log"
LOGFILE_DIR = "rtl_433_processing"
LOGFILE_FILENAME = f"{LOGFILE_PATH}/{LOGFILE_DIR}/rtl_433_processing.log"

LOG_LEVEL = logging.INFO
LOGFILE_MAX_BYTES = 2048
LOGFILE_BACKUP_COUNT = 5

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


# ################# publish_to_mqtt  #########################


def publish_to_mqtt(json_data):
    """Publishes the json data to MQTT"""
    client = mqtt.Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.connect(MQTT_BROKER_ADDRESS, MQTT_BROKER_PORT)

    client.publish("mqtt_topic", json.dumps(json_data))

    client.disconnect()


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
        publish_to_mqtt(transformed_data)


# ################# MAIN #########################


def main():
    """Define input file a standard input and call consume_transform_publish"""

    # Define the input file
    input_file = sys.stdin

    # now do the bulk of the work
    consume_transform_publish(input_file)


if __name__ == "__main__":
    main()
