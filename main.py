#!/usr/bin/env python3
"""
main.py
-------
Python Port Scanner - CLI entrypoint.

Usage examples:
    python main.py -t 192.168.1.1
    python main.py -t scanme.nmap.org -p 1-1024
    python main.py -t 192.168.1.1 -p top --banners
    python main.py -t 192.168.1.1 -p 22,80,443 --output report.json
    python main.py --sweep 192.168.1

⚠️  Only scan systems you own or have explicit permission to test.
"""

import argparse
import sys
from datetime import datetime

from scanner.host_discovery import resolve_host, sweep_subnet
from scanner.port_scanner import scan_host, parse_port_range
from scanner.banner_grabber import enrich_results
from scanner.report_generator import (
    print_banner,
    print_results_table,
    print_summary,
    save_json,
    colorize,
    Color,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="port-scanner",
        description="🔍 Python Port Scanner — Educational TCP connect scanner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
examples:
  python main.py -t 192.168.1.1
  python main.py -t scanme.nmap.org -p 1-1024
  python main.py -t 192.168.1.1 -p top --banners
  python main.py -t 192.168.1.1 -p 22,80,443 --output results.json
  python main.py --sweep 192.168.1

⚠️  Only use on systems you own or have permission to test.
        """,
    )

    target_group = parser.add_mutually_exclusive_group(required=True)
    target_group.add_argument(
        "-t", "--target",
        metavar="HOST",
        help="Target IP address or hostname"
    )
    target_group.add_argument(
        "--sweep",
        metavar="SUBNET",
        help="Ping sweep a /24 subnet (e.g. 192.168.1)"
    )

    parser.add_argument(
        "-p", "--ports",
        default="1-1024",
        metavar="PORTS",
        help="Port range: '1-1024', '22,80,443', 'top', or '1-65535' (default: 1-1024)"
    )
    parser.add_argument(
        "--banners",
        action="store_true",
        help="Attempt to grab service banners from open ports"
    )
    parser.add_argument(
        "--threads",
        type=int,
        default=100,
        metavar="N",
        help="Number of concurrent threads (default: 100)"
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=0.5,
        metavar="SEC",
        help="Per-port timeout in seconds (default: 0.5)"
    )
    parser.add_argument(
        "--output",
        metavar="FILE",
        help="Save results to a JSON file"
    )

    return parser


def run_scan(args: argparse.Namespace) -> None:
    """Execute a single-host scan."""

    # 1. Resolve host
    try:
        ip = resolve_host(args.target)
    except ValueError as e:
        print(colorize(str(e), Color.RED))
        sys.exit(1)

    # 2. Parse port range
    try:
        ports = parse_port_range(args.ports)
    except ValueError:
        print(colorize("[!] Invalid port specification.", Color.RED))
        sys.exit(1)

    # 3. Print scan header
    start_time = datetime.now()
    print_banner(args.target, ip, start_time)
    print(colorize(f"  [*] Scanning {len(ports)} port(s) with {args.threads} threads...\n",
                   Color.CYAN))

    # 4. Scan
    results = scan_host(
        host=ip,
        ports=ports,
        threads=args.threads,
        timeout=args.timeout,
        open_only=True,
    )

    # 5. Banner grab (optional)
    if args.banners and results:
        print(colorize("  [*] Grabbing banners...\n", Color.CYAN))
        enrich_results(ip, results)

    # 6. Print results
    print_results_table(results)

    elapsed = (datetime.now() - start_time).total_seconds()
    print_summary(results, elapsed)

    # 7. Save JSON report (optional)
    if args.output:
        save_json(args.target, ip, results, start_time, elapsed, args.output)


def run_sweep(args: argparse.Namespace) -> None:
    """Execute a subnet ping sweep."""
    print(colorize(f"\n[*] Sweeping {args.sweep}.0/24 ...\n", Color.CYAN))
    live = sweep_subnet(args.sweep)

    if live:
        print(colorize(f"  [+] {len(live)} host(s) found:\n", Color.GREEN))
        for host in live:
            print(f"      {host}")
    else:
        print(colorize("  [!] No live hosts found.", Color.RED))
    print()


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.sweep:
        run_sweep(args)
    else:
        run_scan(args)


if __name__ == "__main__":
    main()
