<<<<<<< HEAD
# krish
About me
🎓 Cybersecurity student | 💻 Python & Linux Enthusiast | 🔐 Aspiring Security Analyst

## 🚀 About Me
- 🧠 Currently learning: Ethical Hacking, Network Security, and Python scripting
- 🛠️ Working on: My GitHub portfolio and cybersecurity labs
- 🌱 Interested in: Penetration Testing, SOC analysis, Red Team/Blue Team
- 🧰 Tools I use: Wireshark, Nmap, Burp Suite, Kali Linux, Git, Python
=======
# 🔍 Python Port Scanner

A small **educational TCP connect port scanner** written in Python using only the standard `socket` library.  
This tool is intended **only** for learning and testing on machines/networks you own or are authorized to scan.

<p align="left">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.7%2B-blue.svg">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-green.svg">
  <img alt="Build" src="https://img.shields.io/badge/CI-GitHub%20Actions-lightgrey">
</p>

## ✨ Features
- Resolves hostnames to IP addresses
- Scans a range of ports (current default 1–1024)
- Prints open ports in real time
- Graceful handling of invalid hosts and keyboard interruption

## 🚀 Quick Start (current version)
Run the script and enter a target when prompted:
```bash
python port_scanner.py
# then enter a host (IP or domain) when asked
```

Example session:
```
Enter host to scan(IP or domain): example.com
--------------------------------------------------
Scanning Target: 93.184.216.34
Scanning started at: 2025-11-11 00:00:00.000000
--------------------------------------------------
port 22 is OPEN
port 80 is OPEN
Scanning completed.
```

## 🧪 Examples
See `examples/sample_scan.txt` for a captured run. You can paste your own results there or add screenshots in an `assets/` folder and link them here.

## 🗺️ Roadmap (nice-to-have improvements)
- **Argparse CLI**: `-t/--target`, `-p/--ports`, `--timeout`, `--threads`
- **Threading / Concurrency** for speed (`threading` / `concurrent.futures`)
- **Custom port ranges**: `-p 22,80,443` or `-p 1-65535`
- **Export formats**: JSON / CSV summary
- **Better error handling** and logging
- **Unit tests** for helpers (e.g., port parsing)

## ⚙️ Requirements
- Python 3.7+
- No external dependencies

## 🧰 Development
Run tests (if you add any) with:
```bash
pytest -q
```

## 🔒 Safety & Legal
Only scan systems you own or have explicit permission to test. Unauthorized scanning may be illegal.  
This project is for **educational** purposes.

## 🪪 License
MIT — see `LICENSE`.

---

### What I learned (add to your résumé)
- Python socket programming and TCP connect scans
- Basic error handling and user interaction
- Project packaging (README, LICENSE, tests, CI)
>>>>>>> 632a8f5 (inital commit)
