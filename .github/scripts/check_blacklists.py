import requests
from datetime import datetime

# File paths
BLACKLISTS_URL_FILE = 'blacklists.fqdn.urls'
BLACKLIST_MONITOR_MD = 'blacklists_monitor.md'

def get_last_modified(url):
    response = requests.head(url)
    if 'Last-Modified' in response.headers:
        return response.headers['Last-Modified']
    return "N/A"

def main():
    with open(BLACKLISTS_URL_FILE, 'r') as f:
        urls = [line.strip() for line in f]

    table_data = []
    for url in urls:
        last_modified = get_last_modified(url)
        table_data.append((url, last_modified))

    # Update the markdown file
    with open(BLACKLIST_MONITOR_MD, 'w') as f:
        f.write("# Blacklists Monitor\n\n")
        f.write("| URL | Last Modified |\n")
        f.write("| --- | ------------- |\n")
        for data in table_data:
            f.write(f"| {data[0]} | {data[1]} |\n")

if __name__ == '__main__':
    main()
