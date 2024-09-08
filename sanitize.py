import re
import tldextract
from tqdm import tqdm
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Pre-compiled regex pattern for FQDN validation
fqdn_pattern = re.compile(r'^(?!-)[A-Za-z0-9-]{1,63}(?<!-)$')
suffix_list = tldextract.SUFFIX_LIST  # List of valid suffixes

def is_valid_fqdn(s):
    """Check if the string is a valid FQDN."""
    if not s or '*' in s:
        return False
    extracted = tldextract.extract(s)
    domain_valid = fqdn_pattern.match(extracted.domain)
    suffix_valid = fqdn_pattern.match(extracted.suffix)
    return domain_valid and suffix_valid and extracted.suffix in suffix_list

def remove_prefixes(line, prefixes):
    """Remove specified prefixes from a line efficiently."""
    for prefix in prefixes:
        if line.startswith(prefix):
            return line[len(prefix):].strip()
    return line

def sanitize_line(line, rules):
    """Apply all sanitization rules to a line."""
    line = line.strip()
    for rule in rules:
        line = rule(line)
        if line is None:
            return None
    return line

def get_sanitization_rules():
    """Returns a list of sanitization rules."""
    return [
        lambda line: None if line.startswith("#") else line,       # Remove comment lines
        lambda line: remove_prefixes(line, ["127.0.0.1", "0.0.0.0", "||", "http://", "https://"]),  # Remove prefixes
        lambda line: line.rstrip('.'),                             # Remove trailing dot
        lambda line: line.lower()                                  # Convert to lowercase
    ]

def process_lines(file_path, rules):
    """Generator to process lines from a file."""
    with open(file_path, 'r') as infile:
        for line in infile:
            sanitized_line = sanitize_line(line, rules)
            if sanitized_line and is_valid_fqdn(sanitized_line):
                yield sanitized_line

def process_large_file(input_file_path, output_file_path):
    """Process large files line by line."""
    start_time = time.time()
    unique_domains = set()
    rules = get_sanitization_rules()

    try:
        for sanitized_line in tqdm(process_lines(input_file_path, rules), desc="Processing"):
            unique_domains.add(sanitized_line)
    except FileNotFoundError:
        logging.error(f"File not found: {input_file_path}")
        return
    except IOError as e:
        logging.error(f"IOError: {e}")
        return

    # Sort the unique domain names in alphabetical order
    sorted_unique_domains = sorted(unique_domains)

    try:
        # Batch write the sorted unique domain names to the output file
        with open(output_file_path, 'w') as outfile:
            for domain in tqdm(sorted_unique_domains, desc="Writing"):
                outfile.write(f"{domain}\n")
    except IOError as e:
        logging.error(f"IOError: {e}")

    end_time = time.time()
    logging.info(f"Processing complete. Time taken: {end_time - start_time:.2f} seconds")

# Use this function to process your large file
process_large_file('input.txt', 'output.txt')
