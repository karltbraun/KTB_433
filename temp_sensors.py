import json
import bounded_stack as bs
from dataclasses import dataclass
from transform_maps import model_map, id_map
from collections import deque

# ######################### round string value  #########################


def round_str_value(temperature_F: str) -> str:
    """Rounds a string value to the nearest integer value and returns it as a string"""
    return str(round(float(temperature_F)))


# ######################### Sensor_Dev_1 class  #########################
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
        def format1() -> str:
            return (
                f"{self.id_name:<{self.fldsiz_id_name}}"
                f"{self.sensor_name:<{self.fldsiz_sensor_name}}"
                f"'{self.model_raw:<{self.fldsiz_model_raw}}'"
                f"{self.model_name:<{self.fldsiz_model_name}}"
                f"'{self.time_raw:<{self.fldsiz_time_raw}}'"
                f"{self.time_date:<{self.fldsiz_time_date}}"
                f"{self.time_time:<{self.fldsiz_time_time}}"
                f"'{self.temperature_raw:<{self.fldsiz_temperature_raw}}'"
                f"{self.temperature_value_f:<{self.fldsiz_temperature_value}}"
                f"{self.temperature_value_c:<{self.fldsiz_temperature_value}}"
                f"'{self.humidity_raw:<{self.fldsiz_humidity_raw}}'"
                f"{self.humidity_value:<{self.fldsiz_humidity_value}}"
                f"{self.channel:^{self.fldsiz_channel}}"
                f"{self.battery:<{self.fldsiz_battery}}"
                f"{self.integrity:<{self.fldsiz_integrity}}"
            )

        def format2() -> str:
            return (
                f"ID:   {self.id_raw:<20}ID_NAME: {self.id_name:<{self.fldsiz_id_name}}"
                f"Name: {self.sensor_name:<20}Model Raw: {self.model_raw:<20}Model Name: {self.model_name:<20}"
                f"TimeR:{self.time_raw:<20}Date: {self.time_date:<20}Time: {self.time_time:<20}"
                f"TempR:{self.temperature_raw:<20}TempF: {self.temperature_value_f:<20}TempC: {self.temperature_value_c:<20}"
                f"Hum_R:{self.humidity_raw:<20}Hum_V: {self.humidity_value:<20}"
                f"Chan: {self.channel:<20}Batt: {self.battery:<20}Integ: {self.integrity:<20}"
            )

        temperature_raw = f"'{self.temperature_raw}'"
        temperature_F = f"{self.temperature_value_f} F"
        temperature_C = f"{self.temperature_value_c} C"
        humidity_raw = f"'{self.humidity_raw}'"
        humidity_value = f"{self.humidity_value} %"
        time_raw = f"'{self.time_raw}'"
        # return format1()
        return format2()

    # ###############################################################################
    #                               class methods                                   #
    # ###############################################################################

    # ############################ from_json #################################

    @classmethod
    def from_json(cls, json_data: dict):
        sensor_obj = cls("<TMP>")  # create object with temp ID

        #! maybe this should be in transform_maps
        dummy_sensor_id_map_data = {
            "id_sensor_name": "UNK S_ID",
            "sensor_name": "UNK SENSOR",
        }

        data = json.loads(json_data)
        # print("---------")
        # print("Creating sensor object from:")
        # pprint(data)

        # ID and Sensor Name
        if "id" not in data:
            sensor_obj.id_raw = ""
            sensor_obj.id_name = "NO_ID"
            sensor_obj.sensor_name = "UNKN SENSOR"
        else:
            sensor_obj.id_raw = data["id"]
            sensor_id_data = id_map.get(sensor_obj.id_raw, dummy_sensor_id_map_data)
            # print(f"<<< type: {type(sensor_id_data)} - {sensor_id_data}")
            sensor_obj.id_name = sensor_id_data["id_sensor_name"]
            sensor_obj.sensor_name = sensor_id_data["sensor_name"]

        # MODEL
        if "model" not in data:
            model = "NO MODEL DATA"
        else:
            model_raw = data["model"]
            model_name = model_map.get(model_raw.upper(), "UKN MODEL")
            sensor_obj.model_raw = model_raw
            sensor_obj.model_name = model_name

        # TIME
        sensor_obj.time_raw = data["time"]
        sensor_obj.time_date, sensor_obj.time_time = sensor_obj.time_raw.split()

        # CHANNEL
        sensor_obj.channel = "CH?"
        if "channel" in data:
            sensor_obj.channel = data["channel"]

        # BATTERY
        sensor_obj.batter = "BAT?"
        if "battery_ok" in data:
            sensor_obj.battery = "OK"
            if data["battery_ok"] != "1":
                sensor_obj.battery = "LOW"

        # TEMPERATURE
        if "temperature_F" in data:
            sensor_obj.temperature_raw = (
                sensor_obj.temperature_value_f
            )  # assume fahrenheit holds the raw value
            sensor_obj.temperature_value_f = round_str_value(data["temperature_F"])
        if "temperature_C" in data:
            # if both F and C values are present, assume the C value is the 'raw' value
            sensor_obj.temperature_raw = sensor_obj.temperature_value_c
            sensor_obj.temperature_value_c = round_str_value(data["temperature_C"])
        # if we have no temperature readings, make the values indicate that
        # if we have an F reading or a C reading, but not the other, calculate the missing value
        if (
            sensor_obj.temperature_value_f == ""
            and sensor_obj.temperature_value_c == ""
        ):
            sensor_obj.temperature_raw = "__"
            sensor_obj.temperature_value_f = "__"
            sensor_obj.temperature_value_c = "__"
        elif sensor_obj.temperature_value_f == "":
            sensor_obj.temperature_value_f = str(
                round(float(sensor_obj.temperature_value_c) * 9 / 5 + 32)
            )
        elif sensor_obj.temperature_value_c == "":
            sensor_obj.temperature_value_c = str(
                round((float(sensor_obj.temperature_value_f) - 32) * 5 / 9)
            )

        # HUMIDITY
        if "humidity" in data:
            sensor_obj.humidity_raw = data["humidity"]
        else:
            sensor_obj.humidity_raw = "__"
        sensor_obj.humidity_value = (
            sensor_obj.humidity_raw
        )  # right now, no transformation for humidity

        # INTEGRITY
        if "mic" in data:
            sensor_obj.integrity = data["mic"]
        else:
            sensor_obj.integrity = "__"
        if sensor_obj.integrity == "CHECKSUM":
            sensor_obj.integrity = "CRC"

        return sensor_obj

    # ############################ to_dict  #################################

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


# ######################### Sensor Stacks #########################


class SensorStacks(dict):
    def __init__(self, max_history=100):
        super().__init__()
        self.max_history = max_history

    def add_reading(self, sensor_id, reading):
        if sensor_id not in self:
            self[sensor_id] = bs.BoundedStack(self.max_history)
        self[sensor_id].push(reading)

    def pop(self, sensor_id):
        return self[sensor_id].pop()

    def size(self, sensor_id):
        return len(self[sensor_id])

    def get_all(self, sensor_id):
        return self[sensor_id].get_all()

    def clear(self, sensor_id):
        return self[sensor_id].clear()
