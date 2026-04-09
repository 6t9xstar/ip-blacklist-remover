import sys
import argparse
import time
import os
import json
from datetime import datetime
from colorama import Fore, Style, init

# Import our custom modules
from scanner import perform_scan, get_public_ip
from diagnosis import run_diagnosis
from cleanup import run_cleanup_check
from delisting import get_delisting_info
from bot import run_spamhaus_bot, run_uceprotect_bot

init(autoreset=True)

BANNER = rf"""
{Fore.CYAN}  _____ _____    _____ _                         
{Fore.CYAN} |_   _|  __ \  / ____| |                        
{Fore.CYAN}   | | | |__) | | |    | | ___  __ _ _ __   ___ _ __ 
{Fore.CYAN}   | | |  ___/  | |    | |/ _ \/ _` | '_ \ / _ \ '__|
{Fore.CYAN}  _| |_| |      | |____| |  __/ (_| | | | |  __/ |   
{Fore.CYAN} |_____|_|       \_____|_|\___|\__,_|_| |_|\___|_|   
                                                     
{Fore.YELLOW}      IP BLACKLIST REMOVER & REPUTATION CLEANER
{Fore.WHITE}      -----------------------------------------
"""

def print_banner():
    print(BANNER)

def save_log(data):
    """Saves scan results to a local JSON file for history."""
    log_file = "scan_history.json"
    history = []
    if os.path.exists(log_file):
        try:
            with open(log_file, "r") as f:
                history = json.load(f)
        except Exception:
            pass
            
    history.append({
        "timestamp": datetime.now().isoformat(),
        "ip": data.get("ip"),
        "listings_count": len(data.get("listed", [])),
        "status": "DIRTY" if data.get("listed") else "CLEAN"
    })
    
    with open(log_file, "w") as f:
        json.dump(history, f, indent=4)

def run_full_scan(ip=None):
    """Executes the full suite: Scan -> Diagnosis -> Cleanup -> Advice."""
    print_banner()
    
    # 1. Scanner
    scan_results = perform_scan(ip)
    save_log(scan_results)
    
    # 2. Diagnosis
    diag_results = run_diagnosis(scan_results['ip'])
    
    # 3. Cleanup Audit
    cleanup_results = run_cleanup_check()
    
    # 4. Delisting Assistant
    get_delisting_info(scan_results['listed'], scan_results['ip'])
    
    if scan_results['listed']:
        print(f"\n{Fore.YELLOW}[!] DETECTED {len(scan_results['listed'])} LISTINGS.")
        choice = input(f"{Fore.CYAN}[?] Would you like to launch the Automation Bot? (y/n): ").lower()
        if choice == 'y':
            start_bot_flow(scan_results['ip'])
    
    print(f"\n{Fore.GREEN}[*] Scan Complete. Review the results above for actions.")

def start_bot_flow(ip, email=None):
    """Interactive flow to start the semi-automated delisting bot."""
    if not email:
        print(f"{Fore.YELLOW}[!] The bot requires an email address to fill the forms.")
        email = input(f"{Fore.CYAN}[?] Enter email for delisting requests: ")
    
    print(f"\n{Fore.MAGENTA}[*] Launching Automation Bot...")
    # Auto-target Spamhaus for now as it is the most critical
    run_spamhaus_bot(ip, email)

def main():
    parser = argparse.ArgumentParser(description="IP Blacklist Remover & Reputation Cleaner")
    parser.add_argument("command", choices=["check", "diagnose", "clean", "full", "monitor", "bot"], 
                        help="Command to run", nargs="?", default="full")
    parser.add_argument("--ip", help="Specific IP to scan (defaults to current public IP)")
    parser.add_argument("--email", help="Email to use for the delisting bot")
    
    args = parser.parse_args()
    
    if args.command == "check":
        perform_scan(args.ip)
    elif args.command == "diagnose":
        ip = args.ip or get_public_ip()
        run_diagnosis(ip)
    elif args.command == "clean":
        run_cleanup_check()
    elif args.command == "bot":
        ip = args.ip or get_public_ip()
        start_bot_flow(ip, args.email)
    elif args.command == "full":
        run_full_scan(args.ip)
    elif args.command == "monitor":
        print(f"{Fore.CYAN}[*] Starting Monitoring Mode... (Ctrl+C to stop)")
        while True:
            run_full_scan(args.ip)
            print(f"\n{Fore.YELLOW}[*] Sleeping for 24 hours until next scheduled scan...")
            time.sleep(86400) # 24 hours

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Process stopped by user.")
        sys.exit(0)
