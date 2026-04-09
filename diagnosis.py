import socket
import smtplib
import requests
from colorama import Fore, Style, init

init(autoreset=True)

def check_ptr(ip):
    """Performs a Reverse DNS lookup for the IP."""
    try:
        hostname, alias, _ = socket.gethostbyaddr(ip)
        return hostname
    except Exception:
        return None

def check_smtp_relay(ip):
    """Checks if the IP has port 25 open (common for SMTP relays)."""
    try:
        # We just try to connect and see if it responds
        with socket.create_connection((ip, 25), timeout=3):
            return True
    except Exception:
        return False

def check_ip_type(ip):
    """Heuristic to guess if IP is Data Center, Residential, or VPN."""
    try:
        # Using a free geo-ip API for metadata
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
        if response.get("status") == "success":
            isp = response.get("isp", "").lower()
            org = response.get("org", "").lower()
            
            dc_keywords = ["aws", "azure", "google", "digitalocean", "linode", "vultr", "ovh", "hosting", "datacenter"]
            for kw in dc_keywords:
                if kw in isp or kw in org:
                    return "Data Center / Hosting", response.get("isp")
            
            return "Likely Residential", response.get("isp")
    except Exception:
        pass
    return "Unknown", "Unknown"

def run_diagnosis(ip):
    """Runs a complete diagnostic suite on the IP."""
    print(f"{Fore.CYAN}[*] Running Diagnosis Engine for {Fore.YELLOW}{ip}...")
    
    ptr = check_ptr(ip)
    relay = check_smtp_relay(ip)
    ip_type, isp = check_ip_type(ip)
    
    results = {
        "ip": ip,
        "ptr": ptr,
        "open_relay": relay,
        "type": ip_type,
        "isp": isp
    }
    
    print(f"\n{Fore.WHITE}--- Diagnostic Results ---")
    
    # PTR Status
    if ptr:
        print(f"{Fore.GREEN}[+] PTR Record Found: {Fore.WHITE}{ptr}")
    else:
        print(f"{Fore.RED}[!] No PTR Record found! (Critical for email deliverability)")
        
    # SMTP Relay Status
    if relay:
        print(f"{Fore.RED}[!] Port 25 (SMTP) is OPEN. Potential Open Relay risk!")
    else:
        print(f"{Fore.GREEN}[+] Port 25 is closed (Safe).")
        
    # IP Type
    color = Fore.YELLOW if "Data Center" in ip_type else Fore.GREEN
    print(f"{Fore.CYAN}[*] IP Type: {color}{ip_type} {Fore.WHITE}(ISP: {isp})")
    
    return results

if __name__ == "__main__":
    from scanner import get_public_ip
    run_diagnosis(get_public_ip())
