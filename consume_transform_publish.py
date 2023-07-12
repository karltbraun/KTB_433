"""consume_transform_publish"""
import json
import sys
import paho.mqtt.client as mqtt
from transform_maps import id_map, model_map
from mqtt_secrets import (
    MQTT_BROKER_ADDRESS,
    MQTT_BROKER_PORT,
    MQTT_USERNAME,
    MQTT_PASSWORD,
)


# ################# publish_to_mqtt  #########################


def publish_to_mqtt(json_data):
    client = mqtt.Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.connect(MQTT_BROKER_ADDRESS, MQTT_BROKER_PORT)

    client.publish("mqtt_topic", json.dumps(json_data))

    client.disconnect()


# ################# transform_json_data #########################


def transform_json_data(json_data):
    # Perform necessary transformations on the JSON data using the id_map and model_map dictionaries
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
    for line in file:
        try:
            json_data = json.loads(line)
            transformed_data = transform_json_data(json_data)
            # Publish the transformed data to MQTT
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON data - {line.strip()}")
        except Exception as e:
            print(f"Error: Failed to process JSON data - {str(e)}")

        publish_to_mqtt(transformed_data)


# ################# MAIN #########################


def main():
    input_file = sys.stdin
    consume_transform_publish(input_file)


if __name__ == "__main__":
    main()
