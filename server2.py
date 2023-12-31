import flask
import os
import json

app = flask.Flask(__name__)

# Define the path to the JSON file and the waiting time as constants
JSON_FILE_PATH = "/Users/karlbraun/"
JSON_FILE_NAME = "data.json"
JSON_FILE_SPEC = f"{JSON_FILE_PATH}/{JSON_FILE_NAME}"
WEBSERVER_PORT = 8080

WAITING_TIME = 5  # seconds


@app.route("/")
def index():
    # Read the JSON file and parse it as a dictionary
    with open(JSON_FILE_SPEC, "r") as f:
        data = json.load(f)

    # Print the contents of the JSON file as plain text
    return str(data)


if __name__ == "__main__":
    app.run(port=WEBSERVER_PORT)
