import time
import sys
from playwright.sync_api import sync_playwright
from colorama import Fore, Style, init

init(autoreset=True)

# Pre-written templates for the bot
DEFAULT_REASON = "fixed security hole, removed malicious scripts, and hardened SMTP configuration. verified no spam is leaving the network."

def run_spamhaus_bot(ip, email, reason=DEFAULT_REASON):
    """
    Launches a semi-automated browser session to Spamhaus.
    Auto-fills the IP and waits for user CAPTCHA.
    """
    print(f"\n{Fore.CYAN}[*] Launching Spamhaus Automation Bot for {Fore.YELLOW}{ip}...")
    print(f"{Fore.MAGENTA}[!] IMPORTANT: You must solve the CAPTCHA manually when it appears.")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) # Headed mode is required for manual CAPTCHA
        context = browser.new_context()
        page = context.new_page()
        
        try:
            # 1. Start Lookup
            page.goto("https://check.spamhaus.org/")
            
            # Wait for search box (handling Cloudflare wall)
            print(f"{Fore.CYAN}[*] Waiting for search box (Solve any Cloudflare check if prompted)...")
            page.wait_for_selector("input#ip-search", timeout=60000)
            
            page.fill("input#ip-search", ip)
            page.press("input#ip-search", "Enter")
            
            print(f"{Fore.GREEN}[+] IP Search submitted. Checking results...")
            time.sleep(3) # Wait for page load
            
            # 2. Inform user
            print(f"\n{Fore.YELLOW}[STEP 1]: If you are listed, click 'Show Details' -> 'Next Step' in the browser.")
            print(f"{Fore.YELLOW}[STEP 2]: Once you reach the form, the bot can attempt to fill it, or you can paste this:")
            print(f"{Fore.WHITE}   Email: {email}")
            print(f"{Fore.WHITE}   Reason: {reason}")
            
            # Keeping the browser open
            print(f"\n{Fore.CYAN}[*] Browser is active. Complete your delisting request.")
            print(f"{Fore.CYAN}[*] Close the browser window when you are finished.")
            
            while True:
                if page.is_closed():
                    break
                time.sleep(1)
                
        except Exception as e:
            print(f"{Fore.RED}[!] Bot Error: {e}")
        finally:
            browser.close()

def run_uceprotect_bot(ip):
    """Semi-automated navigation to UCEPROTECT lookup."""
    print(f"\n{Fore.CYAN}[*] Launching UCEPROTECT Automation Bot for {Fore.YELLOW}{ip}...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        try:
            page.goto("https://www.uceprotect.net/en/rblcheck.php")
            page.fill("input[name='ipr']", ip)
            page.click("input[type='submit']")
            
            print(f"\n{Fore.YELLOW}[INFO]: UCEPROTECT L2/L3 cannot be manually delisted.")
            print(f"{Fore.YELLOW}[INFO]: If you see an L1 listing, follow the 'Removal' button on that page.")
            
            print(f"\n{Fore.CYAN}[*] Browser is active. Close it when finished.")
            while True:
                if page.is_closed():
                    break
                time.sleep(1)
        except Exception as e:
            print(f"{Fore.RED}[!] Bot Error: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python bot.py <ip> <email> <target:spamhaus/uce>")
        sys.exit(1)
    
    ip_addr = sys.argv[1]
    user_email = sys.argv[2]
    target = sys.argv[3] if len(sys.argv) > 3 else "spamhaus"
    
    if target == "spamhaus":
        run_spamhaus_bot(ip_addr, user_email)
    elif target == "uce":
        run_uceprotect_bot(ip_addr)
