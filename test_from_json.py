import sys
from temp_sensors import Sensor_Dev_1

# ########################### MAIN #########################


def main():
    for line in sys.stdin:
        line = line.strip()
        if line:
            sensor = Sensor_Dev_1.from_json(line)
            print(sensor)


if __name__ == "__main__":
    main()
    exit(0)
