import os
import psutil
import subprocess
from colorama import Fore, Style, init

init(autoreset=True)

# Common indicators of spam scripts or malicious mailers
SPAM_KEYWORDS = [
    "mail(", "fsockopen", "pfsockopen", "eval(base64_decode", 
    "system(", "passthru(", "exec(", "shell_exec("
]

# Processes that might be unauthorized mail servers or botnet clients
SUSPICIOUS_PROCESS_NAMES = ["sendmail", "postfix", "exim", "qmail", "smtp", "masscan", "zmap"]

def scan_processes():
    """Scans running processes for potential spam-related activity."""
    print(f"{Fore.CYAN}[*] Scanning running processes...")
    found_procs = []
    
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        try:
            name = proc.info['name'].lower()
            for kw in SUSPICIOUS_PROCESS_NAMES:
                if kw in name:
                    found_procs.append(proc.info)
                    break
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
            
    return found_procs

def scan_for_spam_scripts(start_dir="."):
    """Recursively scans a directory for files containing spam mailer keywords."""
    print(f"{Fore.CYAN}[*] Scanning for suspicious scripts in: {Fore.YELLOW}{os.path.abspath(start_dir)}")
    suspicious_files = []
    
    # We limit the scan to certain extensions to be efficient
    exts = ('.php', '.pl', '.py', '.sh', '.asp', '.aspx')
    
    for root, dirs, files in os.walk(start_dir):
        # Skip common non-malware directories to save time
        if any(skip in root for skip in ["node_modules", ".git", "venv", ".gemini"]):
            continue
            
        for file in files:
            if file.lower().endswith(exts):
                path = os.path.join(root, file)
                
                # Skip the scanner scripts themselves to avoid false positives
                if os.path.basename(path) in ["cleanup.py", "scanner.py"]:
                    continue
                    
                try:
                    with open(path, "r", errors="ignore") as f:
                        content = f.read()
                        for kw in SPAM_KEYWORDS:
                            if kw in content:
                                suspicious_files.append((path, kw))
                                break
                except Exception:
                    pass
                    
    return suspicious_files

def check_mail_queues():
    """Checks if there are high volumes of mail in local queues (Linux only mostly)."""
    # On Windows, we check if the 'Simple Mail Transfer Protocol (SMTP)' service is running
    print(f"{Fore.CYAN}[*] Checking mail server status...")
    if os.name == 'nt':
        try:
            output = subprocess.check_output(["sc", "query", "smtpsvc"], stderr=subprocess.STDOUT).decode()
            if "RUNNING" in output:
                return True, "Windows SMTP Service is RUNNING (Potential spam source if not configured)"
        except Exception:
            pass
    else:
        # Simple check for common linux mail queue commands
        for cmd in ["mailq", "postqueue -p"]:
            try:
                subprocess.check_output(cmd.split(), stderr=subprocess.STDOUT)
                return True, f"Mail queue found via {cmd}"
            except Exception:
                pass
                
    return False, "No local mail server service detected."

def run_cleanup_check():
    """Runs all cleanup-related checks."""
    print(f"{Fore.CYAN}[*] Starting Cleanup & Security Audit Engine...")
    
    procs = scan_processes()
    scripts = scan_for_spam_scripts()
    queue_exists, queue_msg = check_mail_queues()
    
    print(f"\n{Fore.WHITE}--- Cleanup Audit Results ---")
    
    # Process Results
    if procs:
        print(f"{Fore.RED}[!] Suspicious processes detected:")
        for p in procs:
            print(f"  - PID {p['pid']}: {p['name']} ({p['username']})")
    else:
        print(f"{Fore.GREEN}[+] No suspicious mail-related processes found.")
        
    # Script Results
    if scripts:
        print(f"{Fore.RED}[!] Potential spam scripts found ({len(scripts)}):")
        for path, kw in scripts[:10]: # Limit output
            print(f"  - {path} (Trigger: {kw})")
        if len(scripts) > 10:
            print(f"  ... and {len(scripts)-10} more.")
    else:
        print(f"{Fore.GREEN}[+] No obvious spam scripts detected in current directory.")
        
    # Queue Results
    if queue_exists:
        print(f"{Fore.YELLOW}[!] {queue_msg}")
    else:
        print(f"{Fore.GREEN}[+] {queue_msg}")
        
    return {"processes": procs, "scripts": scripts, "queue": queue_msg}

if __name__ == "__main__":
    run_cleanup_check()
