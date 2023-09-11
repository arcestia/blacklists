import os
import requests
from tqdm import tqdm
from datetime import datetime

# File paths
BLACKLISTS_URL_FILE = 'blacklists.fqdn.urls'
BLACKLIST_MONITOR_MD = 'blacklists_monitor.md'
TEMP_DOWNLOAD_PATH = 'temp_download_file'

def get_last_modified(url):
    try:
        if 'raw.githubusercontent.com' in url:
            # Download the file temporarily
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(TEMP_DOWNLOAD_PATH, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            # Check the file's modified time
            file_time = os.path.getmtime(TEMP_DOWNLOAD_PATH)
            return datetime.utcfromtimestamp(file_time).strftime('%Y-%m-%d %H:%M:%S UTC')
        else:
            response = requests.head(url, timeout=10)
            if response.status_code == 200 and 'Last-Modified' in response.headers:
                return response.headers['Last-Modified']
            return "N/A"
    except requests.RequestException:
        return "Error"
    finally:
        # Cleanup the temporary file if it exists
        if os.path.exists(TEMP_DOWNLOAD_PATH):
            os.remove(TEMP_DOWNLOAD_PATH)

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
