# 🔍 Python Port Scanner

A fast, multithreaded **TCP connect port scanner** written in pure Python.  
Built to demonstrate network reconnaissance concepts used in real penetration testing engagements.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat)
![Tests](https://img.shields.io/badge/Tests-Passing-22c55e?style=flat&logo=github-actions)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey?style=flat)

> ⚠️ **For authorized use only.** Only scan systems you own or have explicit written permission to test.  
> See [Legal & Ethical Use](#-legal--ethical-use).

---

## ✨ Features

| Feature | Details |
|---|---|
| 🔎 **Host discovery** | ICMP ping sweep across a /24 subnet |
| ⚡ **Multithreaded scanning** | 100 concurrent threads — scans 1024 ports in ~5 seconds |
| 🏷️ **Service identification** | Detects 20+ common services (SSH, HTTP, FTP, RDP…) |
| 📡 **Banner grabbing** | Pulls version strings from open ports |
| 📊 **JSON reports** | Machine-readable output for further analysis |
| 🎛️ **Flexible CLI** | Custom port ranges, thread count, and timeout |
| 🧪 **Unit tested** | 15+ tests with mocked sockets — no real network needed |
| ✅ **CI/CD** | GitHub Actions tests on Python 3.10, 3.11, 3.12 |

---

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/krishkapila-hckr/python-port-scanner.git
cd python-port-scanner

# No external dependencies — just run it
python main.py -t 127.0.0.1
```

---

## 🎛️ Usage

```
usage: port-scanner [-h] (-t HOST | --sweep SUBNET) [-p PORTS]
                    [--banners] [--threads N] [--timeout SEC] [--output FILE]
```

### Examples

```bash
# Scan top common ports on a host
python main.py -t 192.168.1.1

# Scan a specific port range
python main.py -t scanme.nmap.org -p 1-1024

# Scan specific ports with banner grabbing
python main.py -t 192.168.1.1 -p 22,80,443 --banners

# Save results to JSON
python main.py -t 192.168.1.1 -p top --output report.json

# Ping sweep a subnet to find live hosts
python main.py --sweep 192.168.1
```

### Port Range Syntax

| Syntax | Example | Result |
|---|---|---|
| Single port | `80` | Port 80 only |
| Range | `1-1024` | Ports 1 through 1024 |
| Comma list | `22,80,443` | Those three ports |
| Top ports | `top` | 22 most targeted ports |

---

## 📊 Sample Output

```
=======================================================
  Python Port Scanner
=======================================================
  Target   : scanme.nmap.org
  IP       : 45.33.32.156
  Started  : 2025-11-11 14:23:01
=======================================================

  [*] Scanning 1024 port(s) with 100 threads...

  PORT     STATE      SERVICE
  ---------------------------------------------
  22       OPEN       SSH-2.0-OpenSSH_6.6.1p1
  80       OPEN       HTTP/1.1 200 OK
  9929     OPEN       unknown
  31337    OPEN       unknown

=======================================================
  4 open port(s) found  |  Scan completed in 4.87s
=======================================================
```

See [`sample_output/scan_report.json`](sample_output/scan_report.json) for the full JSON report format.

---

## 🏗️ Project Structure

```
python-port-scanner/
├── main.py                        ← CLI entrypoint (argparse)
├── requirements.txt
├── LICENSE
├── scanner/
│   ├── host_discovery.py          ← ICMP ping sweep, hostname resolution
│   ├── port_scanner.py            ← Multithreaded TCP connect scan
│   ├── banner_grabber.py          ← Service banner fingerprinting
│   └── report_generator.py       ← Terminal table + JSON output
├── tests/
│   └── test_scanner.py            ← 15+ unit tests (mocked sockets)
├── sample_output/
│   └── scan_report.json           ← Example scan of scanme.nmap.org
├── docs/
│   └── methodology.md             ← TCP scan internals, ethics, legal info
└── .github/
    └── workflows/tests.yml        ← CI: tests on Python 3.10–3.12
```

---

## 🔬 Security Concepts Demonstrated

**Network Reconnaissance (Pentest Phase 1)**  
This tool simulates the scanning phase of a penetration test — the step that maps out
which hosts are alive and what services they expose before any exploitation begins.

**TCP Connect Scan**  
Completes the full TCP 3-way handshake (SYN → SYN-ACK → ACK) to confirm a port is open,
then immediately resets the connection. No root privileges required.

**Service Fingerprinting**  
Banner grabbing reads the first bytes a service sends on connection — many services
(SSH, FTP, SMTP) announce their software and version, enabling CVE cross-referencing.

**Multithreading for I/O-bound workloads**  
Port scanning is network I/O-bound. Using `ThreadPoolExecutor` with 100 workers
reduces scan time from ~512s (sequential) to ~5s — a 100x improvement.

---

## 🧪 Running Tests

```bash
pip install pytest
pytest tests/ -v
```

Tests use mocked sockets — no real network traffic is generated.

---

## ⚖️ Legal & Ethical Use

This tool is for **educational purposes and authorized security testing only.**

**Legal to scan:**
- `localhost` / `127.0.0.1`
- `scanme.nmap.org` (explicitly authorized by Nmap)
- Your own home lab or virtual machines
- Any network where you have **written authorization**

Unauthorized port scanning may violate the Computer Fraud and Abuse Act (CFAA),
the Computer Misuse Act, or equivalent laws in your jurisdiction.

---

## 📄 License

MIT — see [LICENSE](LICENSE).

---

*Part of my cybersecurity portfolio. See also: [web-vuln-scanner](#) · [soc-automation-lab](#) · [ctf-writeups](#)*
