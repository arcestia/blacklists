"""whitelist"""
import os
from tqdm import tqdm

def read_file(file_path):
    """Read the file and return a set of FQDNs."""
    fqdns = set()
    with open(file_path, 'r') as file:
        for line in tqdm(file, desc=f"Reading {file_path}", unit="lines", leave=False):
            fqdn = line.strip()
            if fqdn:
                fqdns.add(fqdn)
    return fqdns

def write_file(file_path, content):
    """Write a set of FQDNs to the specified file."""
    with open(file_path, 'w') as file:
        file.write('\n'.join(content))

def file_exists_or_exit(file_path):
    """Check if a file exists or exit the program."""
    if not os.path.isfile(file_path):
        print(f"File '{file_path}' not found.")
        exit(1)

def main():
    """Main function to process blacklist and whitelist files."""
    blacklist_file = 'blacklist.txt'
    whitelist_file = 'whitelist.txt'
    output_file = 'filtered_blacklist.txt'

    # Check if files exist
    file_exists_or_exit(blacklist_file)
    file_exists_or_exit(whitelist_file)

    blacklist_fqdns = read_file(blacklist_file)
    whitelist_fqdns = read_file(whitelist_file)

    # Filter out whitelisted FQDNs from the blacklist
    filtered_fqdns = blacklist_fqdns - whitelist_fqdns

    write_file(output_file, filtered_fqdns)

    print(f"{len(blacklist_fqdns)} FQDNs in the blacklist.")
    print(f"{len(whitelist_fqdns)} FQDNs in the whitelist.")
    print(f"{len(filtered_fqdns)} FQDNs after filtering.")


if __name__ == '__main__':
    main()
