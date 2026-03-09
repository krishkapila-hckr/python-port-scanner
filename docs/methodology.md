# Security Methodology & Concepts

## What This Tool Does

This scanner implements **Phase 1 of a penetration test: Reconnaissance & Scanning.**

In a real engagement, a security professional would use this phase to:
1. Identify live hosts on a network
2. Determine which ports are open
3. Fingerprint services to understand the attack surface
4. Feed findings into Phase 2 (Enumeration) and Phase 3 (Exploitation)

---

## TCP Connect Scan — How It Works

This tool performs a **TCP connect scan**, also called a "full connect scan."

```
Client (You)                 Target Host
     |                            |
     |-------- SYN ------------->|   Step 1: Client requests connection
     |<------- SYN-ACK ----------|   Step 2: Host acknowledges (port is OPEN)
     |-------- ACK ------------->|   Step 3: Connection established
     |-------- RST ------------->|   Step 4: We reset immediately (we don't want data)
```

If the port is **closed**, the host responds with `RST` immediately after `SYN`.  
If the port is **filtered** (firewall), there is no response and the connection times out.

### Comparison to Other Scan Types

| Scan Type       | How It Works                  | Requires Root? | Detectability |
|----------------|-------------------------------|----------------|---------------|
| **TCP Connect** | Full 3-way handshake          | No             | High          |
| SYN Scan        | Half-open (SYN only)          | Yes (raw sock) | Medium        |
| UDP Scan        | Sends UDP packets             | Yes            | Low-Medium    |
| NULL/FIN/XMAS   | Malformed flags               | Yes            | Low           |

This tool uses TCP Connect because it requires **no elevated privileges** and works
on all platforms, making it accessible for students and ethical security testing.

---

## Banner Grabbing

When `--banners` is enabled, the scanner connects to open ports and reads
the first bytes the service sends. Many services (SSH, FTP, SMTP) automatically
announce their software version, which helps:

- Identify what software is running
- Cross-reference against known CVEs (e.g., OpenSSH 6.x → check NVD)
- Determine OS fingerprints

---

## Multithreading for Speed

Sequential scanning 1024 ports at 0.5s timeout = **512 seconds**.  
With 100 threads: roughly **5-10 seconds**.

The scanner uses Python's `concurrent.futures.ThreadPoolExecutor` because
port scanning is **I/O-bound** (waiting on network responses), not CPU-bound.
Threading is the correct tool here — multiprocessing would be overkill.

---

## Legal & Ethical Use

> "With great power comes great responsibility."

Port scanning is a **dual-use tool**. It is used by:
- Security professionals assessing their own infrastructure
- Penetration testers with written authorization
- Students learning networking concepts in lab environments

It can also be used maliciously. **Always ensure you have written permission
before scanning any network or host you don't own.**

Unauthorized port scanning may violate:
- The Computer Fraud and Abuse Act (CFAA) in the US
- The Computer Misuse Act in the UK
- Similar laws in most jurisdictions worldwide

### Safe test targets (legal to scan):
- `localhost` / `127.0.0.1` — your own machine
- `scanme.nmap.org` — explicitly authorized by Nmap for testing
- Your own home lab / VMs
- Networks where you have written authorization
