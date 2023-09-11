import requests
from tqdm import tqdm
from datetime import datetime

# File paths
BLACKLISTS_URL_FILE = 'blacklists.fqdn.urls'
BLACKLIST_MONITOR_MD = 'blacklists_monitor.md'

def get_last_modified(url):
    try:
        response = requests.head(url, timeout=10)
        if response.status_code == 200 and 'Last-Modified' in response.headers:
            return response.headers['Last-Modified']
        return "N/A"
    except requests.RequestException:
        return "Error"

def main():
    with open(BLACKLISTS_URL_FILE, 'r') as f:
        urls = [line.strip() for line in f]

    table_data = []
    
    print("Checking blacklist URLs...")
    for url in tqdm(urls, desc="Progress", ncols=100):
        last_modified = get_last_modified(url)
        table_data.append((url, last_modified))

    # Update the markdown file
    with open(BLACKLIST_MONITOR_MD, 'w') as f:
        f.write("# Blacklists Monitor\n\n")
        f.write("| URL | Last Modified |\n")
        f.write("| --- | ------------- |\n")
        for data in table_data:
            f.write(f"| {data[0]} | {data[1]} |\n")

    print("Updated blacklists_monitor.md!")

if __name__ == '__main__':
    main()
