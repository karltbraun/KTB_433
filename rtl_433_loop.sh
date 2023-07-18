#!/bin/bash
# rtl_433_loop.sh
# Run rtl_433 in a loop with a pause in between

# Define the duration and pause time in seconds
DURATION=120
PAUSE_TIME=180

# Run rtl_433 command in the background and pipe the output to your Python scripts
echo "-------------- Starting rtl_433 --------------"
rtl_433 -F json | python3 rtl_433_publish.py &

# Get the PID of the rtl_433 process
RTL_PID=$!

while true; do
    # Sleep for the specified duration
    sleep $DURATION

    # Pause the rtl_433 process by sending a SIGSTOP signal
    echo "-------------- Pausing rtl_433 --------------"
    kill -SIGSTOP $RTL_PID

    # Sleep for the specified pause time
    sleep $PAUSE_TIME

    # Resume the rtl_433 process by sending a SIGCONT signal
    echo "-------------- Resuming rtl_433 --------------"
    kill -SIGCONT $RTL_PID
done
