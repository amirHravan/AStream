#!/bin/bash
# Scenario 2: Short, Proxy
# Usage: ./vm_client_scen2.sh
# Environment Variables:
#   SERVER_IP: DASH Server IP (default: 127.0.0.1)
#   SERVER_PORT: DASH Server Port (default: 8006)
#   PROXY_IP: Proxy IP (default: 127.0.0.1)
#   PROXY_PORT: Proxy Port (default: 8888)
#   LOG_DIR: Directory to save logs (default: ../../ASTREAM_LOGS)

SERVER_IP=${SERVER_IP:-192.168.56.13}
SERVER_PORT=${SERVER_PORT:-8006}
PROXY_IP=${PROXY_IP:-192.168.56.12}
PROXY_PORT=${PROXY_PORT:-8888}
LOG_DIR=${LOG_DIR:-"../../ASTREAM_LOGS"}

mkdir -p "$LOG_DIR"
cd "$(dirname "$0")/../../dist/client"

echo "Running Scenario 2 (Short, Proxy) against $SERVER_IP:$SERVER_PORT via Proxy $PROXY_IP:$PROXY_PORT..."
python3 dash_client.py -m "http://$SERVER_IP:$SERVER_PORT/media/mpd/short/manifest.mpd" -p "basic" --use-pep --pep-host "$PROXY_IP" --pep-port "$PROXY_PORT"
