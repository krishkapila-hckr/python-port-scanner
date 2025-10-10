import socket
import sys
import threading
from datetime import datetime

target = input("Enter host to scan(IP or domain): ")
try:
    target_ip = socket.gethostbyname(target)
except socket.gaierror:
    print("Hostname could not be resolved.")
    sys.exit()


print("-" * 50)
print(f"Scanning Target: {target_ip}")
print(f"Scanning started at: {datetime.now()}")
print("-" * 50)

try:
    for port in range(1, 1025):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        result = s.connect_ex((target_ip, port))

        if result == 0:
            print(f"port{port} is OPEN")
        s.close()
except KeyboardInterrupt:
    print("\nscan innterrupted by user.")
    sys.exit()

print("Scanning completed.")
