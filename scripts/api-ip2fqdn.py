import json
import requests

# Constants
API_ENDPOINT = "https://api-ipres.domainsblacklists.com/resolve"
TIMEOUT = 3
MAX_IPS = 10  # Change this as per your requirement

# Fetch the blacklisted IPs
with open("blacklist.ip.txt", "r") as file:
    IPS = [line.strip() for line in file.readlines()][:MAX_IPS]

RESOLVED_IPS = []

for ip in IPS:
    try:
        response = requests.get(f"{API_ENDPOINT}/{ip}", timeout=TIMEOUT)
        
        if response.status_code != 200:
            continue
        
        data = response.json()
        resolved_name = data.get("fqdn", "").strip()
        
        # Skip NXDOMAIN and non-resolvable IPs
        if not resolved_name or "nxdomain" in resolved_name.lower():
            continue
        
        # Remove trailing dot
        if resolved_name.endswith('.'):
            resolved_name = resolved_name[:-1]
        
        RESOLVED_IPS.append(resolved_name)

    except (requests.RequestException, json.JSONDecodeError):
        pass

# Save to output file
with open("blacklist.ip.resolved.txt", "w") as out_file:
    for name in RESOLVED_IPS:
        out_file.write(name + "\n")
