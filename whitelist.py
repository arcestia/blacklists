import os
from pathlib import Path
import argparse

def read_fqdn_from_file(file_path: Path) -> set:
    """Read the file and return a set of FQDNs."""
    with open(file_path, 'r') as file:
        return {line.strip() for line in file if line.strip()}

def write_fqdn_to_file(file_path: Path, content: set) -> None:
    """Write a set of FQDNs to the specified file."""
    with open(file_path, 'w') as file:
        for fqdn in content:
            file.write(fqdn + '\n')

def main(blacklist_path: Path, whitelist_path: Path, output_path: Path) -> None:
    """Main function to process blacklist and whitelist files."""
    
    try:
        # Read FQDNs from files
        blacklist_fqdns = read_fqdn_from_file(blacklist_path)
        whitelist_fqdns = read_fqdn_from_file(whitelist_path)

        # Filter out whitelisted FQDNs from the blacklist
        filtered_fqdns = blacklist_fqdns - whitelist_fqdns

        # Write filtered FQDNs to output file
        write_fqdn_to_file(output_path, filtered_fqdns)

        print(f"Blacklist: {len(blacklist_fqdns)} FQDNs.")
        print(f"Whitelist: {len(whitelist_fqdns)} FQDNs.")
        print(f"After Filtering: {len(filtered_fqdns)} FQDNs.")
    
    except FileNotFoundError as e:
        print(f"ERROR: File '{e.filename}' not found.")
        exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process blacklist and whitelist files.")
    parser.add_argument('--blacklist', default='blacklist.txt', type=Path, help='Path to blacklist file')
    parser.add_argument('--whitelist', default='whitelist.txt', type=Path, help='Path to whitelist file')
    parser.add_argument('--output', default='filtered_blacklist.txt', type=Path, help='Path to output file')
    
    args = parser.parse_args()

    main(args.blacklist, args.whitelist, args.output)
