"""
banner_grabber.py
-----------------
Attempts to grab service banners from open ports to identify
software versions and help with fingerprinting.
"""

import socket


# HTTP probe — sent to web ports to trigger a response
HTTP_PROBE = b"HEAD / HTTP/1.0\r\nHost: target\r\n\r\n"

# Ports that respond to HTTP probes
HTTP_PORTS = {80, 443, 8080, 8443, 8888}


def grab_banner(host: str, port: int, timeout: float = 2.0) -> str:
    """
    Connect to an open port and attempt to read a banner.

    For HTTP ports, sends a HEAD request to trigger a response.
    For other ports (SSH, FTP, SMTP), the service usually sends
    a banner immediately on connect.

    Returns:
        A cleaned banner string, or empty string if nothing received.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((host, port))

            # Send HTTP probe on web ports
            if port in HTTP_PORTS:
                s.sendall(HTTP_PROBE)

            banner = s.recv(1024).decode("utf-8", errors="ignore").strip()
            # Return only the first line to keep output clean
            return banner.splitlines()[0] if banner else ""

    except (socket.timeout, socket.error, OSError, UnicodeDecodeError):
        return ""


def enrich_results(host: str, port_results: list, timeout: float = 2.0) -> list:
    """
    Take a list of PortResult objects and add banner info to each.
    Modifies port_results in place and returns it.
    """
    for result in port_results:
        if result.state == "open":
            banner = grab_banner(host, result.port, timeout)
            if banner:
                result.service = banner[:60]  # cap at 60 chars for display
    return port_results
