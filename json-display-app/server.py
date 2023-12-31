from flask import Flask, jsonify
import json

app = Flask(__name__)

# Sample JSON data (replace this with your actual JSON data)
json_data = [
    {"sensor_name": "sensor1", "temperature": 25.3, "humidity": 40},
    {"sensor_name": "sensor2", "temperature": 22.8, "humidity": 50},
    {"sensor_name": "unknown", "info": "Some information about a device"},
    {"sensor_name": "sensor3", "temperature": 28.1, "humidity": 55},
]


@app.route("/data", methods=["GET"])
def get_data():
    return jsonify(json_data)


if __name__ == "__main__":
    app.run(port=3001)  # Run the server on port 3001 (you can change this if needed)
