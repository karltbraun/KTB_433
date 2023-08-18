#!/bin/bash
# rtl_433_run.sh
# Run rtl_433 in and pipe to rtl_433_publish.py

# Define the duration and pause time in seconds
DURATION=120
PAUSE_TIME=15

# Log the starting message
logger -t rtl_433_run.sh -p info "Starting rtl_433"

# Run rtl_433 command in the background and pipe the output to your Python scripts
# rtl_433 -F json | python3 /home/karl/bin/RTL_433/rtl_433_publish.py 2> /home/public/rtl_433_publish.out
rtl_433 -F json | python3 /home/karl/bin/RTL_433/rtl_433_publish.py 2> /dev/null

# Get the PID of the rtl_433 process
RTL_PID=$!
logger -t rtl_433_run.sh -p info "Process ID: ${RTL_PID}"


