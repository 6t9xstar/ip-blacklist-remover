# IP Blacklist Delisting Guide

If your IP falls on a blacklist, follow these steps to remove it.

## 🔴 CRITICAL: Fixing the Cause
Before requesting a delist, you **MUST** fix why you were listed, otherwise you will be re-blacklisted immediately (often with a longer penalty).
1. Run `python main.py clean` to find and delete spam scripts.
2. Check your PTR/Reverse DNS settings.
3. Secure your mail server (disable open relays).

---

## 🛠️ Delisting Instructions for Major Lists

### 1. Spamhaus (ZEN, SBL, XBL, PBL)
- **Visit:** [https://check.spamhaus.org/](https://check.spamhaus.org/)
- **Process:** Enter your IP. Follow the instructions. 
- **Tip:** If you are on the **PBL**, it is usually because you are on a residential IP. You can often delist yourself if you have a business need.

### 2. SpamCop (bl.spamcop.net)
- **Visit:** [https://www.spamcop.net/bl.shtml](https://www.spamcop.net/bl.shtml)
- **Process:** SpamCop listings are usually automatic and expire after 24 hours of no reports. If you fixed the spam source, wait 24 hours.

### 3. Barracuda (b.barracudacentral.org)
- **Visit:** [https://www.barracudacentral.org/rbl/removal-request](https://www.barracudacentral.org/rbl/removal-request)
- **Process:** Fill out the form. You need to provide a reason for removal. Use the template in `delisting.py`.

### 4. SORBS (dnsbl.sorbs.net)
- **Visit:** [http://www.sorbs.net/cgi-bin/db](http://www.sorbs.net/cgi-bin/db)
- **Process:** You need to register an account and "open a ticket" for delisting.

### 5. UCEPROTECT (L1, L2, L3)
- **Note:** External delisting from UCEPROTECT can be difficult as they often blacklist entire IP ranges. 
- **Process:** Check [https://www.uceprotect.net/en/rblcheck.php](https://www.uceprotect.net/en/rblcheck.php). Level 1 listings (individual IP) expire after 7 days of no spam.

---

## 📝 Delisting Message Template
Use this message when contacting support:

> "Hello, I have identified and fixed the root cause of the spam activity on IP [YOUR_IP]. I have secured my server, removed malicious scripts, and verified that all outgoing mail is legitimate. Please review our status and delist our IP. Thank you."

---

## 🇵🇰 Special Advice for PTCL / Pakistan Users
Your scan shows you are on a **Residential IP** from PTCL. This is why you see the following:

### 1. UCEPROTECT Level 2 & 3
- **Level 2:** Your local area subnet is blacklisted because of other users.
- **Level 3:** The entire PTCL network/region is blacklisted.
- **Can you fix it?** No. L2 and L3 cannot be delisted by individuals. Only PTCL's network admins can fix this.
- **Super Perfect Fix:** Use a **Dedicated VPS** (DigitalOcean, AWS) or a **Business Static IP** from PTCL, which usually comes with a cleaner reputation.

### 2. Spamhaus PBL (Policy Block List)
- This is **normal**. Almost every home/residential IP in the world is on the PBL.
- It tells mail servers: "This IP should use an SMTP relay (like Gmail) and not send mail directly."
- Since you are using a **Gmail Free Account**, this listing is acceptable, but it can still trigger "Suspicious" flags in some automated filters.

### 3. Missing PTR (Reverse DNS)
- **This is the #1 reason for "Spam" folders.**
- For PTCL, you usually cannot set a PTR record on a standard 10mbps/20mbps home connection.
- **The Solution:** Contact PTCL Support and ask for a **"Static IP with Reverse DNS"** if you are on a business plan. If you are on a home plan, you must ensure you use **Authenticated SMTP (TLS)** through Gmail's servers (Port 587).

---

## 🛡️ Pro-Level Reputation Tips
If you cannot change your IP, do this for 100% Deliverability:
1. **Never send to "Dead" emails:** High bounce rates on a residential IP will lock your Gmail account.
2. **Use Port 587:** Never use Port 25 for sending from home; it's almost always blocked or monitored.
3. **Monitor Daily:** Keep running `python main.py full` to ensure you don't drop to **UCEPROTECT Level 1** (which means *your* specific computer is caught sending spam).
