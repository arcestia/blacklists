#!/bin/bash

# ==============================
# RPZ BLACKLIST UPDATER SCRIPT
# ==============================

# Required commands
REQUIRED_COMMANDS=("wget" "tar" "systemctl" "grep" "mkdir" "cat" "date" "named-checkconf")

# Check if required commands exist
for cmd in "${REQUIRED_COMMANDS[@]}"; do
  command -v $cmd >/dev/null 2>&1 || { echo >&2 "Error: $cmd is required but it's not installed. Exiting."; exit 1; }
done

# Directory to store the RPZ blacklist
RPZ_DIRECTORY="/path/to/store/rpz_blacklist"
# URL of the RPZ blacklist
RPZ_URL="https://github.com/fabriziosalmi/blacklists/raw/main/rpz_blacklist.tar.gz"
# BIND configuration file
BIND_CONFIG="/etc/bind/named.conf.local"

# Ensure the directory exists
mkdir -p $RPZ_DIRECTORY

# Download the latest RPZ blacklist from the repository
wget -O $RPZ_DIRECTORY/rpz_blacklist.tar.gz "$RPZ_URL"

# Extract the blacklist
tar -xzf $RPZ_DIRECTORY/rpz_blacklist.tar.gz -C $RPZ_DIRECTORY

# Check if the configuration is already added to avoid duplicate entries
if ! grep -q "rpz.blacklist" $BIND_CONFIG; then
    # Append configuration to BIND's config file
    echo "zone \"rpz.blacklist\" {
        type master;
        file \"$RPZ_DIRECTORY/rpz_blacklist.txt\";
    };" >> $BIND_CONFIG

    echo "options {
        response-policy { zone \"rpz.blacklist\"; };
    };" >> $BIND_CONFIG
fi

# Check BIND configuration
named-checkconf $BIND_CONFIG
if [ $? -ne 0 ]; then
    echo "Error in BIND configuration. Please check manually!"
    exit 1
fi

echo "Script executed successfully!"

# You can manually reload BIND to apply the new blacklist with: 
# sudo systemctl reload bind9
# Schedule this script using cron to automate the process. 
# For example, to run it daily at 2 AM:
# crontab -e
# Add:
# 0 2 * * * /path/to/this_script/update_rpz_blacklist.sh
