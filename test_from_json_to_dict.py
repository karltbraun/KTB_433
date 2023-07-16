import sys
from temp_sensors2 import Sensor_Dev_1

# ########################### MAIN #########################


def main():
    lst_sensors = []
    lst_dct_sensors = []

    for line in sys.stdin:
        line = line.strip()
        if line:
            sensor = Sensor_Dev_1.from_json(line)
            lst_sensors.append(sensor)

            sensor_json = sensor.to_dict()
            lst_dct_sensors.append(sensor_json)

    print(f"--------------- lst_sensors ({len(lst_sensors)}) ---------------")
    for sensor in lst_sensors:
        print(sensor)

    print(f"--------------- lst_dct_sensors ({len(lst_dct_sensors)}) ---------------")
    for sensor_json in lst_dct_sensors:
        print(sensor_json)


if __name__ == "__main__":
    main()
    exit(0)
