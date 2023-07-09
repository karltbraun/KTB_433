FILENAME_IN = "rtl_433.out"

with open(FILENAME_IN, "r") as f:
    lines = f.readlines()

for line in lines:
    print(line)
