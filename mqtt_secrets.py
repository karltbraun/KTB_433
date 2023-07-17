# mqtt_secrets.py

MQTT_BROKER = "MQTT-ORG"

HIVE_MQTT_BROKER_ADDRESS = "broker.hivemq.com"

MQTT_CONFIG = {
    "MQTT-ORG": {
        "MQTT_BROKER_ADDRESS": "test.mosquitto.org",
        "MQTT_BROKER_PORT": 1883,
        "MQTT_USERNAME": "",
        "MQTT_PASSWORD": "",
    },
    "HIVEMQ": {
        "MQTT_BROKER_ADDRESS": HIVE_MQTT_BROKER_ADDRESS,
        "MQTT_BROKER_PORT": 8883,
        "MQTT_USERNAME": "ktbmes",
        "MQTT_PASSWORD": "KTBMESktbmes2023",
    },
    "KTB-IMAC-LINUX": {
        "MQTT_BROKER_ADDRESS": "10.24.94.78",
        "MQTT_BROKER_PORT": 1883,
        "MQTT_USERNAME": "",
        "MQTT_PASSWORD": "",
    },
    "VULTR-01": {
        "MQTT_BROKER_ADDRESS": "0.0.0.0",
        "MQTT_BROKER_PORT": 1883,
        "MQTT_USERNAME": "",
        "MQTT_PASSWORD": "",
    },
}

# MQTT broker address/URL
MQTT_BROKER_ADDRESS = MQTT_CONFIG[MQTT_BROKER]["MQTT_BROKER_ADDRESS"]

# MQTT broker TCP port
MQTT_BROKER_PORT = MQTT_CONFIG[MQTT_BROKER]["MQTT_BROKER_PORT"]

# MQTT broker username
MQTT_USERNAME = MQTT_CONFIG[MQTT_BROKER]["MQTT_USERNAME"]

# MQTT broker password
MQTT_PASSWORD = MQTT_CONFIG[MQTT_BROKER]["MQTT_PASSWORD"]
