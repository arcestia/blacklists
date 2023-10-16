#!/bin/bash

# Description: Setup script for maintaining a domain blacklist.

# Function to display an error message and exit
die() {
  echo "$1" >&2
  exit 1
}

# Check if running with sudo
[ "$EUID" -eq 0 ] || die "Please run this script with sudo."

# Update and install prerequisites
echo "Updating package list..."
sudo apt-get update || die "Failed to update package list."
echo "Installing required packages..."
sudo apt-get install -y python3 python3-pip pv ncftp || die "Failed to install packages."

# Upgrade Python and pip
echo "Upgrading Python and pip..."
python3 -m ensurepip --upgrade || die "Failed to upgrade pip."
pip3 install --no-cache-dir --upgrade pip setuptools tldextract tqdm || die "Failed to upgrade pip packages."

# Function to download a URL
download_url() {
  local url="$1"
  local random_filename=$(uuidgen | tr -dc '[:alnum:]')

  echo "Downloading blacklist: $url"
  
  if wget -q --progress=bar:force -O "$random_filename.fqdn.list" "$url"; then
    echo "Downloaded: $url"
  else
    echo "Failed to download: $url"
  fi
}

# Download URLs from the list
LISTS="blacklists.fqdn.urls"
echo "Download blacklists"
while read -r url; do
  download_url "$url"
done < "$LISTS"

# Aggregate blacklists
echo "Aggregate blacklists"
cat *.fqdn.list | sort -u > all.fqdn.blacklist
rm -f *.fqdn.list

# Sanitize blacklists
mv all.fqdn.blacklist input.txt
python sanitize.py
mv output.txt all.fqdn.blacklist

# Remove whitelisted domains
mv all.fqdn.blacklist blacklist.txt
python whitelist.py
mv filtered_blacklist.txt all.fqdn.blacklist
rm blacklist.txt input.txt

total_lines_new=$(wc -l < all.fqdn.blacklist)
echo "Total domains: $total_lines_new."
