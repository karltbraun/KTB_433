import sys
from temp_sensors2 import Sensor_Dev_1

# ########################### MAIN #########################


def main():
    lst_sensors = []

    for line in sys.stdin:
        line = line.strip()
        if line:
            sensor = Sensor_Dev_1.from_json(line)
            lst_sensors.append(sensor)
            sensor_json = 
            print(sensor)


if __name__ == "__main__":
    main()
    exit(0)
