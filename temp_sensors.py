from dataclasses import dataclass


@dataclass
class Sensor_Dev_1:
    fldsiz_id: int = 8
    fldsiz_model: int = 21
    fldsiz_name: int = 21
    fldsiz_time_raw: int = 22  # Raw time stamp
    fldsiz_time_time: int = 12  # HH:MM:SS.nn
    fldsiz_time_date: int = 11  # YYYY-MM-DD
    fldsiz_channel: int = 3
    fldsiz_battery: int = 3
    fldsiz_temperature_raw: int = 12
    fldsiz_temperature_value: int = 7
    fldsiz_temperature_units: int = 2
    fldsiz_humidity_raw: int = 8
    fldsiz_humidity_value: int = 4
    fldsiz_humidity_units: int = 2
    fldsiz_integrity: int = 5

    def __init__(self, id: str = "<NULL>"):
        self.id: str = id
        self.name: str = ""
        self.model: str = ""
        self.time_raw: str = ""
        self.time_time: str = ""
        self.time_date: str = ""
        self.channel: str = ""
        self.battery: str = ""
        self.temperature_raw: str = ""
        self.temperature_value_f: str = ""
        self.temperature_value_c: str = ""
        self.humidity_raw: str = ""
        self.humidity_value: str = ""
        self.integrity: str = ""

    def __str__(self):
        temperature_raw = f"'{self.temperature_raw}'"
        humidity_raw = f"'{self.humidity_raw}'"
        time_raw = f"'{self.time_raw}'"
        return (
            f"{self.id:<{self.fldsiz_id}}"
            f"{self.name:<{self.fldsiz_name}}"
            f"{self.model:<{self.fldsiz_model}}"
            f"{time_raw:<{self.fldsiz_time_raw}}"
            f"{self.time_date:<{self.fldsiz_time_date}}"
            f"{self.time_time:<{self.fldsiz_time_time}}"
            f"{temperature_raw:<{self.fldsiz_temperature_raw}}"
            f"{self.temperature_value_c:<{self.fldsiz_temperature_value}}"
            f"{self.temperature_value_f:<{self.fldsiz_temperature_value}}"
            f"{humidity_raw:<{self.fldsiz_humidity_raw}}"
            f"{self.humidity_value:<{self.fldsiz_humidity_value}}"
            f"{self.channel:<{self.fldsiz_channel}}"
            f"{self.battery:<{self.fldsiz_battery}}"
            f"{self.integrity:<{self.fldsiz_integrity}}"
        )

    model_map = {
        "ACURITE-606TX": "ACURITE-606TX",
        "INFACTORY-TH": "SMARTRO-SC91",
    }

    id_map = {"169": "SC91-A", "167": "SC91-B", "211": "SC91-C", "49": "ACRT-01"}

    # @classmethod
    def to_dict(self):
        dct = {
            "ID": self.id,
            "MODEL": self.model,
            "TIME_RAW": self.time_raw,
            "TIME_DATE": self.time_date,
            "TIME_TIME": self.time_time,
            "TEMPERATURE_RAW": self.temperature_raw,
            "TEMPERATURE_VALUE_C": self.temperature_value_c,
            "TEMPERATURE_VALUE_F": self.temperature_value_f,
            "HUMIDITY_RAW": self.humidity_raw,
            "HUMIDITY_VALUE": self.humidity_value,
            "CHANNEL": self.channel,
            "BATTERY": self.battery,
            "INTEGRITY": self.integrity,
        }
        return dct
