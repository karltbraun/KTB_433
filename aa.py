from dataclasses import dataclass

FILENAME_IN = "rtl_433.out"


# ############### class: Dev1 ################


@dataclass
class Dev1:
    fldsiz_model: int = 21
    fldsiz_id: int = 6
    fldsiz_channel: int = 3
    fldsiz_battery: int = 3
    fldsiz_temperature: int = 10
    fldsiz_humidity: int = 5
    fldsiz_itegrity: int = 5
    fldsiz_timestamp: int = 20

    def __init__(
        self, model, ID, Channel, Battery, Temperature, Humidity, Itegrity, Timestamp
    ):
        self.model = model
        self.ID = ID
        self.Channel = Channel
        self.Battery = Battery
        self.Temperature = Temperature
        self.Humidity = Humidity
        self.Itegrity = Itegrity
        self.Timestamp = Timestamp

    def __str__(self):
        return (
            f"{self.model:<{self.fldsiz_model}}"
            f"{self.ID:<{self.fldsiz_id}}"
            f"{self.Channel:<{self.fldsiz_channel}}"
            f"{self.Battery:<{self.fldsiz_battery}}"
            f"{self.Temperature:<{self.fldsiz_temperature}}"
            f"{self.Humidity:<{self.fldsiz_humidity}}"
            f"{self.Itegrity:<{self.fldsiz_itegrity}}"
            f"{self.Timestamp:<{self.fldsiz_timestamp}}"
        )


# ############### Parse out lines ################

#! TODO: put read lines in main, loop throuh in main
#! TODO: Have parse_line return the data from a single read
#! TODO: Put these into a list
#! TODO: Print out the list in different format
#! TODO: -- CSV, -- JSON, -- to console in columnar format


def parse_out_lines(lines):
    for line in lines:
        msg = ""
        line = line.strip().upper()
        words = line.split()
        # print(f"Length of words: {len(words)}")

        # if words[0][0] == "-":
        if len(words) == 160:
            msg = "----------------------------------------"
        if "TIME" in words[0]:
            if len(words) < 2:
                raise ValueError(f"ERROR: bad length of TIME line ({len(words)})")
            date = words[2]
            timestamp = words[3]
            msg = f"Date: {date}  Time: {timestamp}"
        if "MODEL" in words[0]:
            if len(words) < 3:
                raise ValueError(f"ERROR: bad length of MODEL line ({len(words)})")
            model = words[2]
            id = words[-1]
            msg = f"Model: {model}\nID: {id}"
        if "CHANNEL" in words[0]:
            if len(words) < 16:
                raise ValueError(f"ERROR: bad length of CHANNEL line ({len(words)})")
            channel = battery = temperature = units = humidity = integrity = ""
            channel = words[2]
            battery = words[5]
            if "TEMPERATURE" in words[6]:
                temperature = words[7]
                temp_unit = words[8]
            if "HUMIDITY" in words[9]:
                humidity = words[11]
                humidity_unit = words[12]
            if "INTEGRITY" in words[13]:
                itegrity = words[15]
            msg = f"Channel: {channel}\nBattery: {battery}\nTemperature: {temperature} {temp_unit}\nHumidity: {humidity} {humidity_unit}\nIntegrity: {itegrity}"

        print(msg)


# ########################### MAIN #########################

if __name__ == "__main__":
    with open(FILENAME_IN, "r") as f:
        lines = f.readlines()

    dev = None
    parse_out_lines(lines)

    exit(0)
