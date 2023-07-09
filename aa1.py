from dataclasses import dataclass

FILENAME_IN = "rtl_433.out"


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


with open(FILENAME_IN, "r") as f:
    lines = f.readlines()

dev = None

for line in lines:
    line = line.strip().upper()
    if "TIME" in line:
        words = line.split()
        for word in words:
            print(f"'{word}'", end=" ")
        print()
        continue
    if "MODEL" in line:
        words = line.split()
        for word in words:
            print(f"'{word}'", end=" ")
        print()
        continue
    if "CHANNEL" in line:
        words = line.split()
        for word in words:
            print(f"'{word}'", end=" ")
        print()
        continue

    print("-------------------")
