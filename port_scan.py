import socket
import csv
import time
from concurrent.futures import ThreadPoolExecutor


target = input("Enter IP address or hostname: ")

START_PORT = 1
END_PORT = 1024
TIMEOUT = 1
MAX_THREADS = 100

open_ports = []

print(f"\nScanning {target}...\n")

start_time = time.time()


def scan_port(port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(TIMEOUT)

            result = s.connect_ex((target, port))

            if result == 0:
                try:
                    service = socket.getservbyport(port)
                except OSError:
                    service = "Unknown"

                print(f"[+] Port {port:<5} OPEN   ({service})")

                open_ports.append((port, service))

    except Exception:
        pass


with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
    executor.map(scan_port, range(START_PORT, END_PORT + 1))

elapsed = time.time() - start_time

print("\n----------- Scan Complete -----------")
print(f"Open Ports : {len(open_ports)}")
print(f"Time Taken : {elapsed:.2f} seconds")

            
with open("scan_results.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Port", "Service"])

    for port, service in sorted(open_ports):
        writer.writerow([port, service])

print("Results saved to scan_results.csv")