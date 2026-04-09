# 🛡️ IpClean: Professional IP Blacklist Remover & Reputation Recovery

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Email Reputation](https://img.shields.io/badge/Email-Reputation-BrightGreen)](https://github.com/your-username/ip-blacklist-remover)

**IpClean** is a high-performance, automated platform designed to detect, diagnose, and clean IP Blacklist listings. It is specifically engineered for users sending from residential or dedicated IPs who need to maintain 100% email deliverability.

---

## 🚀 Key Features

- **🔍 Multi-Threaded DNSBL Scanner**: Queries 60+ global blacklists (Spamhaus, Barracuda, SpamCop, SORBS, etc.) in seconds.
- **🩺 Reputation Diagnosis**: Heuristic analysis of PTR records, Port 25 vulnerabilities, and IP classification (Residential vs. Data Center).
- **🧹 Security Cleanup Audit**: Scans running processes and local scripts for potential spam mailers and malicious code.
- **🤖 Semi-Automated Delisting Bot**: Powered by **Playwright**, the bot navigates delisting forms for you, auto-fills data, and assists with submission.
- **📊 Interactive Dashboard**: A premium, color-coded CLI dashboard for real-time monitoring.
- **⏰ Daily Monitoring**: Integrated Windows/Linux automation for 24/7 reputation tracking.

---

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/6t9xstar/ip-blacklist-remover.git
cd ip-blacklist-remover
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup Automation (Optional)

```bash
python -m playwright install chromium
```

---

## 📖 Usage

### Full Scan & Cleanup

Run the complete suite to detect listings and audit your system's security.

```bash
python main.py full
```

### Automation Mode (Daily Scan)

Keep the tool running to monitor your IP rep 24/7.

```bash
python main.py monitor
```

### Delisting Bot

Launch the interactive automation bot to request removals.

```bash
python main.py bot --ip YOUR_IP --email yourname@gmail.com
```

---

## 📁 Project Structure

| File            | Description                                            |
| :-------------- | :----------------------------------------------------- |
| `main.py`       | Primary CLI entry point and dashboard logic.           |
| `scanner.py`    | High-speed multi-threaded DNSBL scanning engine.       |
| `diagnosis.py`  | PTR, SMTP Relay, and IP Type diagnosis.                |
| `cleanup.py`    | Local script and process security auditor.             |
| `bot.py`        | Playwright-powered semi-automated delisting assistant. |
| `scheduler.ps1` | Automation script for Windows Task Scheduler.          |

---

## 🇵🇰 Special Note for PTCL / Residential Users

This tool includes specific heuristics and advice for handling **UCEPROTECT L2/L3** and **Spamhaus PBL** listings common in residential IP ranges (like PTCL Pakistan).

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request for any feature requests or bug fixes.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

<p align="center">Made with ❤️ for High-Deliverability Email Systems</p>
