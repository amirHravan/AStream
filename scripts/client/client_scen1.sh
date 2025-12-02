#!/bin/bash
# Scenario 1: Short, No Proxy
# Usage: ./vm_client_scen1.sh
# Environment Variables:
#   SERVER_IP: DASH Server IP (default: 127.0.0.1)
#   SERVER_PORT: DASH Server Port (default: 8006)
#   LOG_DIR: Directory to save logs (default: ../../ASTREAM_LOGS)

SERVER_IP=${SERVER_IP:-192.168.56.13}
SERVER_PORT=${SERVER_PORT:-8006}
LOG_DIR=${LOG_DIR:-"../../ASTREAM_LOGS"}

mkdir -p "$LOG_DIR"
cd "$(dirname "$0")/../../dist/client"

echo "Running Scenario 1 (Short, No Proxy) against $SERVER_IP:$SERVER_PORT..."
python3 dash_client.py -m "http://$SERVER_IP:$SERVER_PORT/media/mpd/short/manifest.mpd" -p "basic"
