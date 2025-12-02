#!/bin/bash
# Starts the Traffic Shaper
# Usage: sudo ./vm_traffic_shaper.sh
# Environment Variables:
#   INTERFACE: Network interface to shape (default: eth0)

INTERFACE=${INTERFACE:-eth1}
LOG_FILE="${LOG_FILE:-traffic_shaper.log}"

if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit 1
fi

cd "$(dirname "$0")/../../dist/server"
echo "Starting Traffic Shaper on $INTERFACE..."
python3 bandwidth_changer.py -i "$INTERFACE" >"$LOG_FILE" 2>&1
