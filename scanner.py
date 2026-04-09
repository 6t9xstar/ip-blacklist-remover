import dns.resolver
import requests
import concurrent.futures
import socket
from colorama import Fore, Style, init

init(autoreset=True)

# Comprehensive list of DNSBL servers
DEFAULT_DNSBL_LIST = [
    "aspews.ext.sorbs.net", "b.barracudacentral.org", "bl.deadbeef.com",
    "bl.emailbasura.org", "bl.spamcop.net", "blackholes.five-ten-sg.com",
    "blacklist.woody.ch", "bogons.cymru.com", "cbl.abuseat.org",
    "cdl.anti-spam.org.cn", "combined.abuse.ch", "combined.rbl.msrbl.net",
    "db.wpbl.info", "dnsbl-1.uceprotect.net", "dnsbl-2.uceprotect.net",
    "dnsbl-3.uceprotect.net", "dnsbl.abuse.ch", "dnsbl.anticaptcha.net",
    "dnsbl.cyberlogic.net", "dnsbl.dronebl.org", "dnsbl.inps.de",
    "dnsbl.sorbs.net", "drone.abuse.ch", "duinv.aupads.org",
    "dul.dnsbl.sorbs.net", "dul.ru", "escalations.dnsbl.sorbs.net",
    "hil.habeas.com", "http.dnsbl.sorbs.net", "intruders.docs.uu.nh",
    "ips.backscatterer.org", "korea.services.net", "l2.apews.org",
    "mail-abuse.blacklist.jippg.org", "misc.dnsbl.sorbs.net",
    "msgid.bl.gweep.ca", "multi.surbl.org", "no-more-funn.moensted.dk",
    "old.dnsbl.sorbs.net", "opm.dnsbl.sorbs.net", "pbl.spamhaus.org",
    "proxy.bl.gweep.ca", "psbl.surriel.com", "rbl.interserver.net",
    "relays.bl.gweep.ca", "relays.bl.kundenserver.de", "relays.nether.net",
    "sbl.spamhaus.org", "smtp.dnsbl.sorbs.net", "socks.dnsbl.sorbs.net",
    "spam.dnsbl.sorbs.net", "spam.olsentech.net", "spam.rbl.msrbl.net",
    "spam.spamrats.com", "spambot.bls.digibase.ca", "spamlist.or.kr",
    "ubl.unsubscore.com", "ucl.unsubscore.com", "virus.rbl.jp",
    "virus.rbl.msrbl.net", "web.dnsbl.sorbs.net", "xbl.spamhaus.org",
    "zen.spamhaus.org"
]

def get_public_ip():
    """Detects the public IP of the current machine."""
    try:
        response = requests.get("https://api.ipify.org", timeout=5)
        if response.status_code == 200:
            return response.text.strip()
    except Exception:
        pass
    
    # Fallback to socket if request fails
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"

def check_dnsbl(ip, dnsbl):
    """Checks if a given IP is listed on a specific DNSBL."""
    try:
        reversed_ip = ".".join(reversed(ip.split(".")))
        query = f"{reversed_ip}.{dnsbl}"
        
        resolver = dns.resolver.Resolver()
        resolver.timeout = 2
        resolver.lifetime = 2
        
        # DNSBL returns an A record if listed
        resolver.resolve(query, "A")
        return dnsbl, True
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers):
        return dnsbl, False
    except Exception:
        return dnsbl, None  # Error during check

def perform_scan(ip=None):
    """Runs a full scan of the IP against all DNSBLs."""
    if not ip:
        ip = get_public_ip()
    
    results = {
        "ip": ip,
        "listed": [],
        "clean": [],
        "errors": []
    }
    
    print(f"{Fore.CYAN}[*] Starting Blacklist Scan for IP: {Fore.YELLOW}{ip}")
    print(f"{Fore.CYAN}[*] Querying {len(DEFAULT_DNSBL_LIST)} DNSBL servers...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        future_to_dnsbl = {executor.submit(check_dnsbl, ip, bl): bl for bl in DEFAULT_DNSBL_LIST}
        
        for future in concurrent.futures.as_completed(future_to_dnsbl):
            dnsbl = future_to_dnsbl[future]
            try:
                bl_name, status = future.result()
                if status is True:
                    results["listed"].append(bl_name)
                elif status is False:
                    results["clean"].append(bl_name)
                else:
                    results["errors"].append(bl_name)
            except Exception:
                results["errors"].append(dnsbl)
                
    return results

if __name__ == "__main__":
    scan_results = perform_scan()
    print(f"\n{Fore.WHITE}{'='*40}")
    print(f"{Fore.CYAN}SCAN SUMMARY for {scan_results['ip']}")
    print(f"{Fore.WHITE}{'='*40}")
    
    if scan_results["listed"]:
        print(f"{Fore.RED}[!] LISTED ON {len(scan_results['listed'])} BLACKLISTS:")
        for bl in scan_results["listed"]:
            print(f"  - {bl}")
    else:
        print(f"{Fore.GREEN}[+] All clean! No listings found on {len(scan_results['clean'])} servers.")
        
    if scan_results["errors"]:
        print(f"{Fore.YELLOW}[?] {len(scan_results['errors'])} lists failed to respond.")
