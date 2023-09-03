import re
import tldextract
from tqdm import tqdm

# Pre-compiled regex pattern for FQDN validation
fqdn_pattern = re.compile('^(?!-)[A-Za-z0-9-]{1,63}(?<!-)$')

def is_valid_fqdn(s):
    """Check if the string is a valid FQDN."""
    if '*' in s:
        return False
    extracted = tldextract.extract(s)
    if not all([extracted.domain, extracted.suffix]):
        return False
    return all(fqdn_pattern.match(x) for x in s.split('.'))

def remove_comment(line):
    """Remove comment lines that start with '#'."""
    return None if line.startswith("#") else line

def remove_ip_prefix_127(line):
    """Remove the IP prefix '127.0.0.1 '."""
    return line.replace("127.0.0.1 ", "", 1) if line.startswith("127.0.0.1 ") else line

def remove_ip_prefix_0(line):
    """Remove the IP prefix '0.0.0.0 '."""
    return line.replace("0.0.0.0 ", "", 1) if line.startswith("0.0.0.0 ") else line

def remove_double_pipe(line):
    """Remove lines that start with '||'."""
    return line.replace("||", "", 1) if line.startswith("||") else line

def remove_http(line):
    """Remove lines that start with 'http://'."""
    return line.replace("http://", "", 1) if line.startswith("http://") else line

def remove_https(line):
    """Remove lines that start with 'https://'."""
    return line.replace("https://", "", 1) if line.startswith("https://") else line

# List of sanitization rules
sanitization_rules = [
    remove_comment,
    remove_ip_prefix_127,
    remove_ip_prefix_0,
    remove_double_pipe,
    remove_http,
    remove_https,
]

def sanitize_line(line):
    """Apply all sanitization rules to a line."""
    line = line.strip()
    for rule in sanitization_rules:
        line = rule(line)
        if line is None:
            return None
    return line if is_valid_fqdn(line) else None

def process_large_file(input_file_path, output_file_path):
    """Process large files line by line."""
    unique_domains = set()
    total_lines = sum(1 for _ in open(input_file_path))

    with open(input_file_path, 'r') as infile:
        for line in tqdm(infile, total=total_lines, desc="Processing"):
            sanitized_line = sanitize_line(line)
            if sanitized_line is not None:
                unique_domains.add(sanitized_line)

    # Sort the unique domain names in alphabetical order
    sorted_unique_domains = sorted(unique_domains)

    # Write the sorted unique domain names to the output file
    with open(output_file_path, 'w') as outfile:
        for domain in tqdm(sorted_unique_domains, desc="Writing"):
            outfile.write(domain + '\n')

# Use this function to process your large file
process_large_file('input.txt', 'output.txt')
