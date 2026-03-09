"""
report_generator.py
--------------------
Formats and outputs scan results as a terminal table and/or JSON file.
"""

import json
import sys
from datetime import datetime


# ANSI color codes for terminal output
class Color:
    GREEN  = "\033[92m"
    RED    = "\033[91m"
    YELLOW = "\033[93m"
    CYAN   = "\033[96m"
    BOLD   = "\033[1m"
    RESET  = "\033[0m"


def _supports_color() -> bool:
    """Check if the terminal supports ANSI colors."""
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


def colorize(text: str, color: str) -> str:
    if _supports_color():
        return f"{color}{text}{Color.RESET}"
    return text


def print_banner(target: str, ip: str, start_time: datetime) -> None:
    """Print the scan header."""
    print(colorize("\n" + "=" * 55, Color.CYAN))
    print(colorize("  Python Port Scanner", Color.BOLD))
    print(colorize("=" * 55, Color.CYAN))
    print(f"  Target   : {colorize(target, Color.YELLOW)}")
    print(f"  IP       : {colorize(ip, Color.YELLOW)}")
    print(f"  Started  : {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(colorize("=" * 55 + "\n", Color.CYAN))


def print_results_table(results: list) -> None:
    """Print open ports in a formatted table."""
    if not results:
        print(colorize("  [!] No open ports found.\n", Color.RED))
        return

    header = f"  {'PORT':<8} {'STATE':<10} {'SERVICE'}"
    print(colorize(header, Color.BOLD))
    print("  " + "-" * 45)

    for r in results:
        state_str = colorize(f"{r.state.upper():<10}", Color.GREEN)
        print(f"  {r.port:<8} {state_str} {r.service}")

    print()


def print_summary(results: list, elapsed: float) -> None:
    """Print scan summary statistics."""
    open_count = sum(1 for r in results if r.state == "open")
    print(colorize("=" * 55, Color.CYAN))
    print(f"  {colorize(str(open_count), Color.GREEN)} open port(s) found  |  "
          f"Scan completed in {colorize(f'{elapsed:.2f}s', Color.YELLOW)}")
    print(colorize("=" * 55 + "\n", Color.CYAN))


def save_json(
    target: str,
    ip: str,
    results: list,
    start_time: datetime,
    elapsed: float,
    filepath: str
) -> None:
    """Save scan results to a JSON file."""
    report = {
        "scan_info": {
            "target": target,
            "ip": ip,
            "timestamp": start_time.isoformat(),
            "duration_seconds": round(elapsed, 2),
        },
        "open_ports": [
            {
                "port": r.port,
                "state": r.state,
                "service": r.service,
            }
            for r in results
            if r.state == "open"
        ],
        "stats": {
            "total_scanned": len(results),
            "open": sum(1 for r in results if r.state == "open"),
        },
    }

    with open(filepath, "w") as f:
        json.dump(report, f, indent=2)

    print(colorize(f"  [+] Report saved to {filepath}\n", Color.GREEN))
