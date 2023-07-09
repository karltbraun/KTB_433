from dataclasses import dataclass
from typing import List, Tuple

FILENAME_IN = "rtl_433.out"


# ############### class: Dev1 ################


@dataclass
class Dev1:
    fldsiz_id: int = 8
    fldsiz_model: int = 21
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

    def __init__(self, id: str):
        self.id: str = id
        self.model: str = ""
        self.time_raw: str = ""
        self.time_time: str = ""
        self.time_date: str = ""
        self.channel: str = ""
        self.battery: str = ""
        self.temperature_raw: str = ""
        self.temperature_value_f: str = ""
        self.temperature_value_c: str = ""
        self.temperature_units: str = ""
        self.humidity_raw: str = ""
        self.humidity_value: str = ""
        self.humidity_units: str = ""
        self.integrity: str = ""

    def __str__(self):
        temperature_raw = f"'{self.temperature_raw}'"
        humidity_raw = f"'{self.humidity_raw}'"
        time_raw = f"'{self.time_raw}'"
        return (
            f"{self.id:<{self.fldsiz_id}}"
            f"{self.model:<{self.fldsiz_model}}"
            f"{time_raw:<{self.fldsiz_time_raw}}"
            f"{self.time_date:<{self.fldsiz_time_date}}"
            f"{self.time_time:<{self.fldsiz_time_time}}"
            f"{temperature_raw:<{self.fldsiz_temperature_raw}}"
            f"{self.temperature_value_c:<{self.fldsiz_temperature_value}}"
            f"{'C':<{self.fldsiz_temperature_units}}"
            f"{self.temperature_value_f:<{self.fldsiz_temperature_value}}"
            f"{'F':<{self.fldsiz_temperature_units}}"
            f"{humidity_raw:<{self.fldsiz_humidity_raw}}"
            f"{self.humidity_value:<{self.fldsiz_humidity_value}}"
            f"{self.humidity_units:<{self.fldsiz_humidity_units}}"
            f"{self.channel:<{self.fldsiz_channel}}"
            f"{self.battery:<{self.fldsiz_battery}}"
            f"{self.integrity:<{self.fldsiz_integrity}}"
        )

    model_map = {
        "ACURITE-606TX": "ACURITE-606TX",
        "INFACTORY-TH": "SMARTRO-SC91",
    }

    id_map = {"169": "SC91-A", "167": "SC91-B", "211": "SC91-C", "49": "ACRT-01"}


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


# ############### Parse out lines ################

#! TODO: Print out the list in different format
#! TODO: -- CSV, -- JSON, -- to console in columnar format


# ############### parse lines ########################


def parse_lines(lines: List[str]) -> List[Dev1]:
    """Parse the lines of the rtl_433.out file and return a list of Dev1 objects"""
    lst_dev = []
    dev1 = None

    for line in lines:
        if "_ _ " in line:
            # device separator
            if dev1 is not None:
                lst_dev.append(dev1)
            dev1 = None
        else:
            # continuation of device
            if dev1 is None:
                # Create a new Dev1 object
                dev1 = Dev1(line.strip())
            # Parse the line and update Dev1 attributes
            parse_line(line, dev1)

    # Add the last Dev1 object to the list
    if dev1 is not None:
        lst_dev.append(dev1)

    return lst_dev


# ############### parse a line ########################


def parse_line(line: str, dev: Dev1) -> None:
    """Parse a line and fill in attribute values"""
    if "- - " in line:
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


# ################## read input file #####################


def read_file(filename: str) -> List[str]:
    """Read the input file and return a list of lines"""
    with open(filename, "r") as f:
        lines = f.readlines()
    return lines


# ########################### MAIN #########################


def main():
    """Main function"""
    MAX_LINES = 100
    lines = read_file("rtl_433.out")

    print("============= Parsing Lines =============")
    lst_devs = parse_lines(lines)

    print(f"============= Printing Device Entries ({len(lst_devs)}) =============")
    i = 0
    for dev in lst_devs:
        if (i := i + 1) > MAX_LINES:
            break
        print(dev)


if __name__ == "__main__":
    main()
