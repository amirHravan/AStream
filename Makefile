# AStream Simulation Makefile

# Configuration Defaults
SERVER_IP ?= 127.0.0.1
SERVER_PORT ?= 8006
PROXY_IP ?= 127.0.0.1
PROXY_PORT ?= 8888
INTERFACE ?= lo
LOG_DIR ?= ASTREAM_LOGS

# Paths
SERVER_DIR = dist/server
PROXY_DIR = dist/proxy
CLIENT_DIR = dist/client

.PHONY: help setup run-server run-shaper run-proxy run-client-scen1 run-client-scen2 run-client-scen3 run-client-scen4 clean

help:
	@echo "AStream Simulation Makefile"
	@echo "Targets:"
	@echo "  setup               - Download and prepare video content"
	@echo "  run-server          - Start DASH Server"
	@echo "  run-shaper          - Start Traffic Shaper (requires sudo)"
	@echo "  run-proxy           - Start Proxy"
	@echo "  run-client-scen1    - Run Client Scenario 1 (Short, No Proxy)"
	@echo "  run-client-scen2    - Run Client Scenario 2 (Short, Proxy)"
	@echo "  run-client-scen3    - Run Client Scenario 3 (Long, No Proxy)"
	@echo "  run-client-scen4    - Run Client Scenario 4 (Long, Proxy)"
	@echo "  clean               - Remove logs"
	@echo ""
	@echo "Variables (can be overridden):"
	@echo "  SERVER_IP, SERVER_PORT, PROXY_IP, PROXY_PORT, INTERFACE, LOG_DIR"

setup:
	cd $(SERVER_DIR) && ./setup_content.sh

run-server:
	@echo "Starting Server on $(SERVER_IP):$(SERVER_PORT)..."
	cd $(SERVER_DIR) && python3 dash_server_py3.py -s 0.0.0.0 -p $(SERVER_PORT)

run-shaper:
	@echo "Starting Traffic Shaper on $(INTERFACE)..."
	cd $(SERVER_DIR) && sudo python3 bandwidth_changer.py -i $(INTERFACE)

run-proxy:
	@echo "Starting Proxy on $(PROXY_IP):$(PROXY_PORT) -> $(SERVER_IP):$(SERVER_PORT)..."
	cd $(PROXY_DIR) && python3 proxy.py --listen-host 0.0.0.0 --listen-port $(PROXY_PORT) --target-host $(SERVER_IP) --target-port $(SERVER_PORT)

run-client-scen1:
	@echo "Running Scenario 1 (Short, No Proxy)..."
	mkdir -p $(LOG_DIR)
	cd $(CLIENT_DIR) && python3 dash_client.py -m "http://$(SERVER_IP):$(SERVER_PORT)/media/mpd/short/manifest.mpd" -p "basic"

run-client-scen2:
	@echo "Running Scenario 2 (Short, Proxy)..."
	mkdir -p $(LOG_DIR)
	cd $(CLIENT_DIR) && python3 dash_client.py -m "http://$(SERVER_IP):$(SERVER_PORT)/media/mpd/short/manifest.mpd" -p "basic" --use-pep --pep-host $(PROXY_IP) --pep-port $(PROXY_PORT)

run-client-scen3:
	@echo "Running Scenario 3 (Long, No Proxy)..."
	mkdir -p $(LOG_DIR)
	cd $(CLIENT_DIR) && python3 dash_client.py -m "http://$(SERVER_IP):$(SERVER_PORT)/media/mpd/long/manifest.mpd" -p "basic"

run-client-scen4:
	@echo "Running Scenario 4 (Long, Proxy)..."
	mkdir -p $(LOG_DIR)
	cd $(CLIENT_DIR) && python3 dash_client.py -m "http://$(SERVER_IP):$(SERVER_PORT)/media/mpd/long/manifest.mpd" -p "basic" --use-pep --pep-host $(PROXY_IP) --pep-port $(PROXY_PORT)

clean:
	rm -rf $(LOG_DIR)
