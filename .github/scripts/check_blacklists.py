import os
import requests
from tqdm import tqdm
from datetime import datetime

# File paths
BLACKLISTS_URL_FILE = 'blacklists.fqdn.urls'
BLACKLIST_MONITOR_MD = 'blacklists_monitor.md'
GITHUB_API_URL = "https://api.github.com/repos/{owner}/{repo}/commits?path={path}"

def get_last_modified(url):
    try:
        if 'raw.githubusercontent.com' in url:
            # Parsing the URL to retrieve repository details
            parts = url.split("/")
            owner = parts[3]
            repo = parts[4]
            path = "/".join(parts[5:])
            api_url = GITHUB_API_URL.format(owner=owner, repo=repo, path=path)

            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()
            if data and 'commit' in data[0] and 'committer' in data[0]['commit']:
                return data[0]['commit']['committer']['date']
            else:
                return "N/A"
        else:
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

    print("Updated blacklists_monitor.md!")

if __name__ == '__main__':
    main()
