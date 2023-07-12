import sys
import json
from dataclasses import dataclass
from temp_sensors import Sensor_Dev_1
from typing import List, Tuple

"""
FILENAME_IN = "rtl_433.out"
FILENAME_OUT = "rtl_433.json"
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


# ############### parse a line ########################


def parse_line(line: str, dev: Sensor_Dev_1) -> None:
    """Parse a line and fill in attribute values"""
    if "- - " in line:
        print(f"Unexpected device separator ({line})")
        return

    msg = ""
    words = line.strip().upper().split()

    if "TIME" in words[0]:
        if len(words) < 2:
            raise ValueError(f"ERROR: bad length of TIME line ({len(words)})")
        dev.time_raw = " ".join(words[2:])
        dev.time_time = words[3]
        dev.time_date = words[2]
        msg = f"time_raw: {dev.time_raw} Date: {dev.time_date} Time: {dev.time_time}"

    elif "MODEL" in words[0]:
        if len(words) < 3:
            raise ValueError(f"ERROR: bad length of MODEL line ({len(words)})")
        dev.model = dev.model_map.get(words[2], "UNKNOWN")
        dev.id = dev.id_map.get(words[-1], "UNK")
        msg = f"Model: {dev.model}\nID: {dev.id}"

    if "BATTERY" in words[0]:  # Accurate 606TX
        if len(words) < 9:
            raise ValueError(
                f"ERROR: bad length of BATTERY line (Accurate) ({len(words)})"
            )
        dev.battery = words[2]
        dev.temperature_raw = " ".join(words[4:6])
        dev.temperature_value_c, dev.temperature_value_f = convert_temperature(
            float(words[4]), words[5]
        )
        dev.integrity = words[-1]
        if dev.integrity == "CHECKSUM":
            dev.integrity = "CRC"
        msg = (
            f"Battery: {dev.battery}\n"
            f"Temperature: {dev.temperature_value_c} C {dev.temperature_value_f} F\n"
            f"Integrity: {dev.integrity}\n"
        )

    if "CHANNEL" in words[0]:  # SMARTRO SC91
        if len(words) < 16:
            raise ValueError(
                f"ERROR: bad length of CHANNEL line (SMARTRO SC91) ({len(words)})"
            )
        dev.channel = (
            dev.battery
        ) = dev.temperature = dev.units = dev.humidity = dev.integrity = ""
        dev.channel = words[2]
        dev.battery = words[5]

        # each of these may or may not be in the line (so NOT elif)

        if "TEMPERATURE" in words[6]:
            dev.temperature_raw = " ".join(words[7:9])
            dev.temperature_value_c, dev.temperature_value_f = convert_temperature(
                float(words[7]), words[8]
            )

        if "HUMIDITY" in words[9]:
            dev.humidity_raw = " ".join(words[11:13])
            dev.humidity_value = words[11]
            dev.humidity_units = words[12]

        if "INTEGRITY" in words[13]:
            dev.integrity = words[-1]

        msg = (
            f"Channel: {dev.channel}\n"
            f"Battery: {dev.battery}\n"
            f"Integrity: {dev.integrity}\n"
            f"Temperature: {dev.temperature_raw} {dev.temperature_value_c} C {dev.temperature_value_f} F\n"
            f"Humidity: {dev.humidity_raw} {dev.humidity_value} {dev.humidity_units}\n"
        )

    print(msg)


# ########################### process_sensor  #########################


def process_sensor(dev: Sensor_Dev_1):
    dev_dict = dev.to_dict()
    json_text = json.dumps(dev_dict)
    print(json_text)
    #! TODO: publish to MQTT instead of printing


# ########################### MAIN #########################


def main():
    dev = None

    for line in sys.stdin:
        if "_ _ " not in line:
            # continue processing the current device
            parse_line(line.strip(), dev)
        else:
            # end of previous device, start a new one
            if dev is not None:
                process_sensor(dev)
            dev = Sensor_Dev_1(id="TBD")

    if dev is not None:
        process_sensor(dev)


if __name__ == "__main__":
    main()
