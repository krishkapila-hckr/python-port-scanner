"""
port_scanner.py
---------------
Multithreaded TCP connect port scanner.
"""

import socket
import concurrent.futures
from dataclasses import dataclass


# Most commonly targeted ports — useful for quick scans
TOP_PORTS = [
    21, 22, 23, 25, 53, 80, 110, 111, 135, 139,
    143, 443, 445, 993, 995, 1723, 3306, 3389,
    5900, 8080, 8443, 8888
]

COMMON_SERVICES = {
    21: "FTP",       22: "SSH",        23: "Telnet",
    25: "SMTP",      53: "DNS",        80: "HTTP",
    110: "POP3",     111: "RPC",       135: "MS-RPC",
    139: "NetBIOS",  143: "IMAP",      443: "HTTPS",
    445: "SMB",      993: "IMAPS",     995: "POP3S",
    1723: "PPTP",    3306: "MySQL",    3389: "RDP",
    5900: "VNC",     8080: "HTTP-Alt", 8443: "HTTPS-Alt",
    8888: "HTTP-Alt"
}


@dataclass
class PortResult:
    port: int
    state: str       # "open" or "closed"
    service: str


def scan_port(host: str, port: int, timeout: float = 0.5) -> PortResult:
    """
    Attempt a TCP connect to a single port.
    Returns a PortResult with state 'open' or 'closed'.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((host, port))
            state = "open" if result == 0 else "closed"
    except (socket.error, OSError):
        state = "closed"

    service = COMMON_SERVICES.get(port, "unknown")
    return PortResult(port=port, state=state, service=service)


def scan_host(
    host: str,
    ports: list[int] | range,
    threads: int = 100,
    timeout: float = 0.5,
    open_only: bool = True
) -> list[PortResult]:
    """
    Scan a list or range of ports on a host using a thread pool.

    Args:
        host:      Target IP address
        ports:     List or range of port numbers
        threads:   Max concurrent threads
        timeout:   Per-port connection timeout in seconds
        open_only: If True, return only open ports

    Returns:
        Sorted list of PortResult objects
    """
    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {
            executor.submit(scan_port, host, port, timeout): port
            for port in ports
        }
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)

    results.sort(key=lambda r: r.port)

    if open_only:
        return [r for r in results if r.state == "open"]
    return results


def parse_port_range(port_arg: str) -> list[int]:
    """
    Parse a port argument string into a list of integers.
    
    Supports:
        "80"           → [80]
        "1-1024"       → [1, 2, ..., 1024]
        "22,80,443"    → [22, 80, 443]
        "top"          → TOP_PORTS list
    """
    if port_arg.lower() == "top":
        return TOP_PORTS

    ports = set()
    for part in port_arg.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            ports.update(range(int(start), int(end) + 1))
        else:
            ports.add(int(part))

    return sorted(ports)
