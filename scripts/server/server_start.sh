#!/bin/bash
# Starts the DASH Server
# Usage: ./vm_server_start.sh
# Environment Variables:
#   SERVER_PORT: Port to listen on (default: 8006)
#   SERVER_IP: IP to listen on (default: 0.0.0.0)

SERVER_PORT=${SERVER_PORT:-8006}
SERVER_IP=${SERVER_IP:-0.0.0.0}
LOG_FILE="${LOG_FILE:-server.log}"

cd "$(dirname "$0")/../../dist/server"
echo "Starting DASH Server on $SERVER_IP:$SERVER_PORT..."
python3 dash_server_py3.py -s "$SERVER_IP" -p "$SERVER_PORT" >"$LOG_FILE" 2>&1
