#!/bin/bash
# rtl_433_loop.sh
# Run rtl_433 in a loop with a pause in between

# Define the duration and pause time in seconds
DURATION=120
PAUSE_TIME=15

# Log the starting message
logger -t rtl_433_loop.sh -p info "Starting rtl_433"
/home/karl/bin/publish_log.sh -t "KTBMES/sensor/logs/rtl_433_loop" -m "Starting rtl_433"

# Run rtl_433 command in the background and pipe the output to your Python scripts
rtl_433 -F json | python3 rtl_433_publish.py &

# Get the PID of the rtl_433 process
RTL_PID=$!

while true; do
    # Sleep for the specified duration
    sleep $DURATION

    # Log the pause message
    logger -t rtl_433_loop.sh -p debug "Pausing rtl_433"
    /home/karl/bin/publish_log.sh -t "KTBMES/sensor/logs/rtl_433_loop" -m "Pausing rtl_433"

    # Pause the rtl_433 process by sending a SIGSTOP signal
    kill -SIGSTOP $RTL_PID

    # Sleep for the specified pause time
    sleep $PAUSE_TIME

    # Log the resume message
    logger -t rtl_433_loop.sh -p debug "Resuming rtl_433"
    /home/karl/bin/publish_log.sh -t "KTBMES/sensor/logs/rtl_433_loop" -m "Resuming rtl_433"

    # Resume the rtl_433 process by sending a SIGCONT signal
    kill -SIGCONT $RTL_PID
done

