#!/bin/bash
# Starts the Proxy
# Usage: ./vm_proxy_start.sh
# Environment Variables:
#   LISTEN_HOST: Host to listen on (default: 0.0.0.0)
#   LISTEN_PORT: Port to listen on (default: 8888)
#   TARGET_HOST: Target DASH Server Host (default: 127.0.0.1)
#   TARGET_PORT: Target DASH Server Port (default: 8006)

LISTEN_HOST=${LISTEN_HOST:-0.0.0.0}
LISTEN_PORT=${LISTEN_PORT:-8888}
TARGET_HOST=${TARGET_HOST:-127.0.0.1}
TARGET_PORT=${TARGET_PORT:-8006}
LOG_FILE="${LOG_FILE:-proxy.log}"

cd "$(dirname "$0")/../../dist/proxy"
echo "Starting Proxy listening on $LISTEN_HOST:$LISTEN_PORT -> $TARGET_HOST:$TARGET_PORT..."
python3 proxy.py --listen-host "$LISTEN_HOST" --listen-port "$LISTEN_PORT" --target-host "$TARGET_HOST" --target-port "$TARGET_PORT" >"$LOG_FILE" 2>&1
