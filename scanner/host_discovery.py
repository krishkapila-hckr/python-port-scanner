"""
host_discovery.py
-----------------
Resolves hostnames and validates targets before scanning.
"""

import socket
import subprocess
import platform
import concurrent.futures


def resolve_host(target: str) -> str:
    """Resolve a hostname or domain to an IP address."""
    try:
        ip = socket.gethostbyname(target)
        return ip
    except socket.gaierror:
        raise ValueError(f"[!] Could not resolve host: '{target}'")


def ping_host(ip: str) -> str | None:
    """
    Send a single ICMP ping to check if a host is alive.
    Returns the IP if alive, None otherwise.
    """
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", "-W", "1", ip]
    try:
        result = subprocess.run(command, capture_output=True, timeout=3)
        return ip if result.returncode == 0 else None
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None


def sweep_subnet(subnet_base: str, threads: int = 50) -> list[str]:
    """
    Perform a ping sweep over a /24 subnet.
    
    Args:
        subnet_base: First 3 octets, e.g. '192.168.1'
        threads: Number of concurrent threads
    
    Returns:
        List of live IP addresses
    """
    targets = [f"{subnet_base}.{i}" for i in range(1, 255)]
    live_hosts = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        results = executor.map(ping_host, targets)

    for result in results:
        if result:
            live_hosts.append(result)

    return sorted(live_hosts)
