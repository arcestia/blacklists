import os
from pathlib import Path
import argparse
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_fqdn_from_file(file_path: Path) -> set:
    """Read the file and return a set of FQDNs."""
    if not file_path.exists():
        logging.error(f"File not found: {file_path}")
        raise FileNotFoundError(file_path)
    
    with file_path.open('r') as file:
        return {line.strip() for line in file if line.strip()}

def write_fqdn_to_file(file_path: Path, content: set) -> None:
    """Write a set of FQDNs to the specified file."""
    with file_path.open('w') as file:
        for fqdn in content:
            file.write(f"{fqdn}\n")

def main(blacklist_path: Path, whitelist_path: Path, output_path: Path) -> None:
    """Main function to process blacklist and whitelist files."""
    start_time = time.time()
    
    try:
        # Read FQDNs from files
        blacklist_fqdns = read_fqdn_from_file(blacklist_path)
        whitelist_fqdns = read_fqdn_from_file(whitelist_path)

        # Filter out whitelisted FQDNs from the blacklist
        filtered_fqdns = blacklist_fqdns - whitelist_fqdns

        # Write filtered FQDNs to output file
        write_fqdn_to_file(output_path, filtered_fqdns)

        logging.info(f"Blacklist: {len(blacklist_fqdns)} FQDNs.")
        logging.info(f"Whitelist: {len(whitelist_fqdns)} FQDNs.")
        logging.info(f"After Filtering: {len(filtered_fqdns)} FQDNs.")
    
    except FileNotFoundError as e:
        logging.error(f"File not found: {e.filename}")
        exit(1)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        exit(1)
    
    end_time = time.time()
    logging.info(f"Processing complete. Time taken: {end_time - start_time:.2f} seconds")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process blacklist and whitelist files.")
    parser.add_argument('--blacklist', default='blacklist.txt', type=Path, help='Path to blacklist file')
    parser.add_argument('--whitelist', default='whitelist.txt', type=Path, help='Path to whitelist file')
    parser.add_argument('--output', default='filtered_blacklist.txt', type=Path, help='Path to output file')
    
    args = parser.parse_args()

    main(args.blacklist, args.whitelist, args.output)
