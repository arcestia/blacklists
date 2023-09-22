#!/bin/bash

# WARNING: Review this script carefully to avoid unintended consequences on your systems and services.

# Function to display error messages
print_error() {
  echo "Error: $1" >&2
  exit 1
}

# Function to display success messages
print_success() {
  echo "Success: $1"
}

# Function to validate a domain name using a more precise regex
validate_domain() {
  local domain="$1"
  local domain_regex="^((?!-)[A-Za-z0-9-]{1,63}(?<!-)\.)+[A-Za-z]{2,63}$"
  if [[ ! "$domain" =~ $domain_regex ]]; then
    print_error "Invalid domain name: $domain"
  fi
}

# Constants
readonly BLACKLIST_URL="https://github.com/fabriziosalmi/blacklists/releases/download/latest/blacklist.txt"
readonly INPUT_FILE="/tmp/all.fqdn.blacklist"
readonly RULES_FILE="nftables_rules.nft"
readonly TABLE_NAME="filter"
readonly CHAIN_NAME="input_drop"

# Download the blacklist from GitHub
if ! wget -q -O "$INPUT_FILE" "$BLACKLIST_URL"; then
  print_error "Failed to download the blacklist from $BLACKLIST_URL"
fi

# Ensure the input file exists and is readable
if [[ ! -r "$INPUT_FILE" ]]; then
  print_error "Input file not found or not readable: $INPUT_FILE"
fi

# Initialize the nftables rules file
{
  echo "#!/usr/sbin/nft -f"
  echo "flush ruleset"
  echo "table $TABLE_NAME {"
  echo "    chain $CHAIN_NAME {"
  
  # Process each domain from the input file
  while IFS= read -r domain || [[ -n "$domain" ]]; do
    validate_domain "$domain" # Validate the domain name before adding the rule
    echo "        drop ip daddr $domain"
    echo "        drop ip saddr $domain"
  done < "$INPUT_FILE"
  
  echo "    }"
  echo "}"
} > "$RULES_FILE"

# Apply the rules using nft
if ! nft -f "$RULES_FILE"; then
  print_error "Error applying nftables rules. Ensure you have the necessary privileges."
else
  print_success "nftables rules applied successfully."
fi

# Cleanup
rm -f "$INPUT_FILE" "$RULES_FILE"
