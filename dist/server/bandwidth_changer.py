__author__ = 'pjuluri'

import subprocess
import time
import sys
import signal
import argparse
import datetime

# Configuration
HIGH_BW = "8mbit"  # 1MB/s
LOW_BW = "1mbit"    # 128KB/s
INITIAL_WAIT = 90   # Wait 90s before starting the pattern
HIGH_DURATION = 90  # Run normally for 90s
LOW_DURATION = 30   # Drop for 30s

def run_command(cmd):
    # print(f"Executing: {cmd}")
    subprocess.check_call(cmd, shell=True)

def cleanup(interface):
    print(f"\nCleaning up traffic shaping on {interface}...")
    try:
        run_command(f"sudo tc qdisc del dev {interface} root")
    except subprocess.CalledProcessError:
        pass
    print("Done.")
    sys.exit(0)

def setup_tc(interface):
    print(f"Setting up TC on {interface}...")
    # Clear existing
    try:
        run_command(f"sudo tc qdisc del dev {interface} root 2>/dev/null")
    except:
        pass
    
    # Add root HTB
    run_command(f"sudo tc qdisc add dev {interface} root handle 1: htb default 10")
    # Add default class
    run_command(f"sudo tc class add dev {interface} parent 1: classid 1:10 htb rate {HIGH_BW}")

def change_bw(interface, rate):
    run_command(f"sudo tc class change dev {interface} parent 1: classid 1:10 htb rate {rate}")

def run_changer(interface):
    # Handle Ctrl+C
    signal.signal(signal.SIGINT, lambda sig, frame: cleanup(interface))
    signal.signal(signal.SIGTERM, lambda sig, frame: cleanup(interface))

    print(f"Starting Traffic Shaper on {interface}")
    print(f"Pattern: Initial Wait {INITIAL_WAIT}s -> Loop: {LOW_BW} ({LOW_DURATION}s) <-> {HIGH_BW} ({HIGH_DURATION}s)")
    
    setup_tc(interface)

    # Initial Wait
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{current_time}] Initial High Bandwidth: {HIGH_BW} for {INITIAL_WAIT}s")
    change_bw(interface, HIGH_BW)
    time.sleep(INITIAL_WAIT)

    while True:
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{current_time}] Setting Low Bandwidth: {LOW_BW} (DROP)")
        change_bw(interface, LOW_BW)
        time.sleep(LOW_DURATION)

        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{current_time}] Setting High Bandwidth: {HIGH_BW}")
        change_bw(interface, HIGH_BW)
        time.sleep(HIGH_DURATION)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="AStream Bandwidth Changer")
    parser.add_argument("-i", "--interface", help="Network interface to shape", default="lo")
    args = parser.parse_args()
    
    run_changer(args.interface)
