from colorama import Fore, Style, init

init(autoreset=True)

# Map of major DNSBLs to their removal/delisting request pages
DELISTING_URLS = {
    "zen.spamhaus.org": "https://check.spamhaus.org/",
    "sbl.spamhaus.org": "https://check.spamhaus.org/",
    "xbl.spamhaus.org": "https://check.spamhaus.org/",
    "pbl.spamhaus.org": "https://check.spamhaus.org/",
    "bl.spamcop.net": "https://www.spamcop.net/bl.shtml",
    "dnsbl.sorbs.net": "http://www.sorbs.net/cgi-bin/db",
    "b.barracudacentral.org": "https://www.barracudacentral.org/rbl/removal-request",
    "dnsbl-1.uceprotect.net": "https://www.uceprotect.net/en/rblcheck.php",
    "dnsbl-2.uceprotect.net": "https://www.uceprotect.net/en/rblcheck.php",
    "dnsbl-3.uceprotect.net": "https://www.uceprotect.net/en/rblcheck.php",
    "psbl.surriel.com": "https://psbl.org/listing",
    "ubl.unsubscore.com": "https://www.unsubscore.com/lookup.php",
    "db.wpbl.info": "http://www.wpbl.info/lookup",
    "dnsbl.abuse.ch": "https://abuse.ch/dnsbl/",
    "spam.spamrats.com": "https://www.spamrats.com/lookup.php",
    "cbl.abuseat.org": "https://www.abuseat.org/lookup.cgi",
    "multi.surbl.org": "http://www.surbl.org/lookup"
}

# The "Super Perfect" message template as requested in the blueprint
DELISTING_TEMPLATE = """
--- DELISTING REQUEST TEMPLATE ---
Subject: Delisting Request for IP: {ip}

Hello Support Team,

I am writing to request the removal of my IP address ({ip}) from your blacklist.

I have taken the following corrective actions:
1. Conducted a full security audit of the server/machine.
2. Identified and removed the source of spam activity (secured compromised scripts).
3. Verified that no unauthorized mail is leaving the network.
4. Hardened the SMTP configuration and confirmed proper PTR/Reverse DNS setup.

Please verify the current status and process the delisting request.

Thank you for your assistance.
----------------------------------
"""

def get_delisting_info(listed_bls, ip):
    """Provides links and templates for delisting based on current listings."""
    print(f"\n{Fore.CYAN}[*] Generating Delisting Assistant Report for {Fore.YELLOW}{ip}...")
    
    if not listed_bls:
        print(f"{Fore.GREEN}[+] No listings detected. No delisting needed!")
        return
    
    print(f"\n{Fore.YELLOW}REMOVAL LINKS:")
    for bl in listed_bls:
        url = DELISTING_URLS.get(bl, "https://www.google.com/search?q=" + bl + "+delisting")
        print(f"  - {Fore.WHITE}{bl}: {Fore.CYAN}{url}")
        
    print(f"\n{Fore.YELLOW}SUGGESTED MESSAGE:")
    print(Fore.WHITE + DELISTING_TEMPLATE.format(ip=ip))
    
    print(f"{Fore.MAGENTA}[!] IMPORTANT: Delisting is usually manual. Visit the links above to submit requests.")

if __name__ == "__main__":
    # Test call
    get_delisting_info(["zen.spamhaus.org", "bl.spamcop.net"], "1.2.3.4")
