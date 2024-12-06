import os
import requests
from collections import Counter
import subprocess

# Configuration
LATEST_BLACKLIST_URL = "https://github.com/fabriziosalmi/blacklists/releases/download/latest/blacklist.txt"
BLACKLIST_FILE = "blacklist.txt"
PREVIOUS_FILE = "previous_blacklist.txt"

def download_blacklist(url, output_file):
    """Download the latest blacklist from the URL."""
    print(f"Downloading latest blacklist from {url}...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"Blacklist saved to {output_file}.")
    except requests.RequestException as e:
        print(f"Error downloading blacklist: {e}")
        exit(1)

def get_previous_blacklist(output_file):
    """Retrieve the previous blacklist using git."""
    try:
        # First check if we're in a git repository
        subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], 
                      check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Check if we have at least 2 commits
        result = subprocess.run(["git", "rev-list", "--count", "HEAD"],
                              capture_output=True, text=True, check=True)
        commit_count = int(result.stdout.strip())
        
        if commit_count < 2:
            print("Warning: Repository has less than 2 commits. Using empty previous blacklist.")
            with open(output_file, 'w') as f:
                f.write("")
            return

        # Try to get the previous version
        subprocess.run(
            ["git", "show", "HEAD~1:" + BLACKLIST_FILE],
            stdout=open(output_file, 'w'),
            stderr=subprocess.PIPE,
            check=True
        )
        print(f"Previous blacklist saved to {output_file}.")
    except subprocess.CalledProcessError as e:
        print(f"Warning: Unable to retrieve previous blacklist. Using empty file. Error: {e}")
        with open(output_file, 'w') as f:
            f.write("")

def load_blacklist(file_path):
    """Load a blacklist file into a set of domains."""
    if not os.path.exists(file_path):
        return set()
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return {line.strip() for line in f if line.strip()}
    except UnicodeDecodeError:
        # Fallback to latin-1 if UTF-8 fails
        with open(file_path, 'r', encoding='latin-1') as f:
            return {line.strip() for line in f if line.strip()}

def calculate_stats(current, previous):
    """Calculate statistics between the current and previous blacklists."""
    stats = {
        "total_domains": len(current),
        "unique_domains": len(current),
        "added_domains": len(current - previous),
        "removed_domains": len(previous - current),
        "tld_distribution": Counter(domain.split('.')[-1] for domain in current if '.' in domain)
    }
    return stats

def display_stats(stats):
    """Display statistics in the terminal."""
    print("\n=== Blacklist Statistics ===")
    print(f"Total Domains: {stats['total_domains']:,}")
    print(f"Unique Domains: {stats['unique_domains']:,}")
    print(f"Added Domains Since Last Version: {stats['added_domains']:,}")
    print(f"Removed Domains Since Last Version: {stats['removed_domains']:,}")
    
    print("\nTop-Level Domain Distribution:")
    for tld, count in stats['tld_distribution'].most_common(10):
        print(f"  .{tld}: {count:,}")

def ensure_latest_commits():
    """Fetch the latest two commits to ensure the repository is up-to-date."""
    try:
        print("Fetching the latest two commits...")
        subprocess.run(["git", "fetch", "--depth", "2"], 
                      check=True, stderr=subprocess.PIPE)
        print("Fetched the latest two commits successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Warning: Error fetching commits: {e}")
        # Continue execution even if fetch fails

def main():
    # Step 1: Fetch the latest commits
    ensure_latest_commits()
    
    # Step 2: Download the latest blacklist
    download_blacklist(LATEST_BLACKLIST_URL, BLACKLIST_FILE)
    
    # Step 3: Retrieve the previous blacklist from git
    get_previous_blacklist(PREVIOUS_FILE)
    
    # Step 4: Load current and previous blacklists
    current_blacklist = load_blacklist(BLACKLIST_FILE)
    previous_blacklist = load_blacklist(PREVIOUS_FILE)
    
    # Step 5: Calculate stats
    stats = calculate_stats(current_blacklist, previous_blacklist)
    
    # Step 6: Display stats
    display_stats(stats)

if __name__ == "__main__":
    main()
