import os
import json
import paho.mqtt.client as mqtt
from mqtt_secrets import (
    MQTT_BROKER_ADDRESS,
    MQTT_BROKER_PORT,
    MQTT_USERNAME,
    MQTT_PASSWORD,
)

# ################ determine the topic ################


def determine_topic(json_data: dict) -> str:
    topic = f"KTBMES/weather/sensor_1/{json_data['id']}"
    return topic


# ################ publish to mqtt  ################


def publish_to_mqtt(json_data: dict, topic: str = "ktb/rtl_433/misc") -> None:
    """First we are going to test by just printing the json message to the console"""
    msg = "{" + topic + json.dumps(json_data) + "}"
    print(msg)
    # return
    """ this is the initial mqtt publish code """
    client = mqtt.Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.connect(MQTT_BROKER_ADDRESS, MQTT_BROKER_PORT)

    client.publish(topic, json.dumps(json_data))

    client.disconnect()


# ################ normalize the json data ################


def normalize_json_data(json_data: dict) -> dict:
    # Perform necessary modifications and mappings on the JSON data
    # Return the modified JSON data

    model_map = {
        "ACURITE-606TX": "ACURITE-606TX",
        "Acurite-606TX": "ACURITE-606TX",
        "INFACTORY-TH": "SMARTRO-SC91",
        "inFactory-TH": "SMARTRO-SC91",
    }

    id_map = {
        "169": "SC91-A",
        169: "SC91-A",
        "167": "SC91-B",
        167: "SC91-B",
        "211": "SC91-C",
        211: "SC91-C",
        "49": "ACRT-01",
        49: "ACRT-01",
    }

    # we want to modify the model: value according the model_map
    # we want to modify the id: value according to the id_map

    if "model" in json_data:
        json_data["model"] = model_map.get(json_data["model"], json_data["model"])

    if "id" in json_data:
        json_data["id"] = id_map.get(json_data["id"], f"{json_data['id']} x")

    return json_data


# ################ consume the json file ################


def consume_json_file(file_path: str) -> None:
    with open(file_path, "r") as file:
        while True:
            line = file.readline()
            if not line:
                break
            json_data = json.loads(line)

            normalized_data = normalize_json_data(json_data)
            topic = determine_topic(json_data)

            publish_to_mqtt(normalized_data, topic)


# ################ MAIN ################


def main():
    FILENAME_IN = "Data/rtl_433.json"

    if not os.path.exists(FILENAME_IN):
        print(f"File not found: {FILENAME_IN}")
        exit(1)

    consume_json_file(FILENAME_IN)


if __name__ == "__main__":
    main()
