import json
from dataclasses import dataclass
from transform_maps import model_map, id_map


@dataclass
class Sensor_Dev_1:
    fldsiz_id_raw: int = 8  # Raw ID from sensor
    fldsiz_id_name: int = 8  # Human friendly name (see id_map)
    fldsiz_sensor_name: int = 21
    fldsiz_model_raw: int = 21
    fldsiz_model_name: int = 21
    fldsiz_time_raw: int = 22  # Raw time stamp
    fldsiz_time_time: int = 12  # HH:MM:SS.nn
    fldsiz_time_date: int = 11  # YYYY-MM-DD
    fldsiz_channel: int = 5
    fldsiz_battery: int = 5
    fldsiz_temperature_raw: int = 12
    fldsiz_temperature_value: int = 10
    fldsiz_temperature_units: int = 2
    fldsiz_humidity_raw: int = 8
    fldsiz_humidity_value: int = 5
    fldsiz_humidity_units: int = 2
    fldsiz_integrity: int = 5

    def __init__(self, id: str = "<NULL>"):
        self.id_raw: str = id  # "raw" id (as provided by device)
        self.id_name: str = ""  # transformed id (into human friendly name)
        self.sensor_name: str = ""  # transformed id (into human friendly name)
        self.model_raw: str = ""  # "raw" model (as provided by device)
        self.model_name: str = ""  # transformed model (into human friendly name)
        self.time_raw: str = ""  # "raw" time (as provided by device)
        self.time_time: str = ""  # transformed time (into HH:MM:SS)
        self.time_date: str = ""  # transformed date (into YYYY-MM-DD)
        self.channel: str = ""
        self.battery: str = ""
        self.temperature_raw: str = ""  # "raw" temperature (as provided by device)
        self.temperature_value_f: str = ""
        self.temperature_value_c: str = ""
        self.humidity_raw: str = ""  # "raw" humidity (as provided by device)
        self.humidity_value: str = ""
        self.integrity: str = ""

    def __str__(self):
        temperature_raw = f"'{self.temperature_raw}'"
        temperature_F = f"{self.temperature_value_f} F"
        temperature_C = f"{self.temperature_value_c} C"
        humidity_raw = f"'{self.humidity_raw}'"
        humidity_value = f"{self.humidity_value} %"
        time_raw = f"'{self.time_raw}'"
        return (
            f"{self.id_name:<{self.fldsiz_id_name}}"
            f"{self.sensor_name:<{self.fldsiz_sensor_name}}"
            f"'{self.model_raw:<{self.fldsiz_model_raw}}'"
            f"{self.model_name:<{self.fldsiz_model_name}}"
            f"{time_raw:<{self.fldsiz_time_raw}}"
            f"{self.time_date:<{self.fldsiz_time_date}}"
            f"{self.time_time:<{self.fldsiz_time_time}}"
            f"{temperature_raw:<{self.fldsiz_temperature_raw}}"
            f"{temperature_F:<{self.fldsiz_temperature_value}}"
            f"{temperature_C:<{self.fldsiz_temperature_value}}"
            f"{humidity_raw:<{self.fldsiz_humidity_raw}}"
            f"{humidity_value:<{self.fldsiz_humidity_value}}"
            f"{self.channel:^{self.fldsiz_channel}}"
            f"{self.battery:<{self.fldsiz_battery}}"
            f"{self.integrity:<{self.fldsiz_integrity}}"
        )

    @classmethod
    def from_json(cls, json_data):
        data = json.loads(json_data)
        obj = cls(data["id"])

        # ID and Sensor Name
        if "id" not in data:
            obj.id_raw = "___"
            obj.id_name = "NO_ID"
            obj.sensor_name = "_____"
        else:
            obj.id_raw = data["id"]
            id_data = id_map.get(obj.id_raw, {})
            obj.id_name = id_data.get("idx", "UNK ID")
            obj.sensor_name = id_data.get("name", "UNKNOWN")

        # MODEL
        if "model" not in data:
            model = "NO MODEL DATA"
        else:
            model_raw = data["model"]
            model_name = model_map.get(model_raw.upper(), "UKN MODEL")
            obj.model_raw = model_raw
            obj.model_name = model_name

        # TIME
        obj.time_raw = data["time"]
        obj.time_date, obj.time_time = obj.time_raw.split()

        # CHANNEL
        obj.channel = "CH?"
        if "channel" in data:
            obj.channel = data["channel"]

        # BATTERY
        obj.batter = "BAT?"
        if "battery_ok" in data:
            obj.battery = "OK"
            if data["battery_ok"] != "1":
                obj.battery = "LOW"

        # TEMPERATURE
        if "temperature_F" in data:
            obj.temperature_value_f = data["temperature_F"]
            obj.temperature_raw = obj.temperature_value_f
        if "temperature_C" in data:
            obj.temperature_value_c = data["temperature_C"]
            obj.temperature_raw = (
                obj.temperature_value_c
            )  # will override F if both are present
        if obj.temperature_value_f == "" and obj.temperature_value_c == "":
            obj.temperature_value_f = "__"
            obj.temperature_value_c = "__"
        elif obj.temperature_value_f == "":
            obj.temperature_value_f = round(obj.temperature_value_c * 9 / 5 + 32, 1)
        elif obj.temperature_value_c == "":
            obj.temperature_value_c = round((obj.temperature_value_f - 32) * 5 / 9, 1)

        # HUMIDITY
        if "humidity" in data:
            obj.humidity_raw = data["humidity"]
        else:
            obj.humidity_raw = "__"
        obj.humidity_value = (
            obj.humidity_raw
        )  # right now, no transformation for humidity

        # INTEGRITY
        if "mic" in data:
            obj.integrity = data["mic"]
        else:
            obj.integrity = "__"
        if obj.integrity == "CHECKSUM":
            obj.integrity = "CRC"

        return obj

    model_map = {
        "ACURITE-606TX": "ACURITE-606TX",
        "INFACTORY-TH": "SMARTRO-SC91",
    }

    id_map = {"169": "SC91-A", "167": "SC91-B", "211": "SC91-C", "49": "ACRT-01"}

    def to_dict(self):
        dct = {
            "id_raw": self.id_raw,
            "sensor_name": self.sensor_name,
            "model_raw": self.model_raw,
            "model_name": self.model_name,
            "time_raw": self.time_raw,
            "time_time": self.time_time,
            "time_date": self.time_date,
            "channel": self.channel,
            "battery_ok": self.battery,
            "temperature_raw": self.temperature_raw,
            "temperature_C": self.temperature_value_c,
            "temperature_F": self.temperature_value_f,
            "humidity_raw": self.humidity_raw,
            "humidity": self.humidity_value,
            "integrity": self.integrity,
        }
        return dct


# ################ Sensor Reading Stack ################
class SensorReadingStack:
    def __init__(self, max_size):
        self.max_size = max_size
        self.stack = []

    def push(self, sensor_reading):
        self.stack.append(sensor_reading)
        if len(self.stack) > self.max_size:
            self.stack = self.stack[
                -self.max_size :
            ]  # Trim the stack to the specified size

    def pop(self):
        if self.stack:
            return self.stack.pop()
        else:
            return None

    def peek(self):
        if self.stack:
            return self.stack[-1]
        else:
            return None

    def is_empty(self):
        return len(self.stack) == 0

    def size(self):
        return len(self.stack)
