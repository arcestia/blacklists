#!/bin/bash

# !! WARNING !!
# please double check this script to avoid any unwanted effect on your systems and services

# Function to display error messages
print_error() {
  echo "Error: $1"
  exit 1
}

# Function to display success messages
print_success() {
  echo "$1"
}

# Function to validate a domain name using regex
validate_domain() {
  local domain=$1
  if [[ ! $domain =~ ^[a-zA-Z0-9.-]+$ ]]; then
    print_error "Invalid domain name: $domain"
  fi
}

# Download blacklist from GitHub
wget -O /tmp/all.fqdn.blacklist https://github.com/fabriziosalmi/blacklists/releases/download/latest/blacklist.txt

# Extract the blacklist
input_file="/tmp/all.fqdn.blacklist"

# Check if the input file exists and is readable
if [ ! -f "$input_file" ] || [ ! -r "$input_file" ]; then
  print_error "Input file not found or not readable: $input_file"
fi

# Define the nftables table and chain names
table_name="filter"
chain_name="input_drop"

# Create the nftables rules file
rules_file="nftables_rules.nft"
echo "#!/usr/sbin/nft -f" > "$rules_file"
echo "flush ruleset" >> "$rules_file"
echo "table $table_name {" >> "$rules_file"
echo "    chain $chain_name {" >> "$rules_file"

# Read the input file line by line and add drop rules for each domain
while read -r domain; do
  if [ -n "$domain" ]; then
    validate_domain "$domain" # Validate the domain name before adding the rule
    echo "        drop ip daddr $domain" >> "$rules_file"
    echo "        drop ip saddr $domain" >> "$rules_file"
  fi
done < "$input_file"

# Add the nftables footer to the rules file
echo "    }" >> "$rules_file"
echo "}" >> "$rules_file"

# Apply the rules using nft
if nft -f "$rules_file"; then
  print_success "nftables rules applied successfully."
else
  print_error "Error applying nftables rules. Make sure you have the necessary privileges."
fi

# Clean up the downloaded and extracted files, and the rules file
rm -f /tmp/all.fqdn.blacklist.tar.gz "$input_file" "$rules_file"
