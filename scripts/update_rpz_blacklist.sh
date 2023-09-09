#!/bin/bash

# Reload BIND to apply the new blacklist: sudo systemctl reload bind9
# Make sure to replace `/path/to/store/rpz_blacklist` with the desired directory path on your server where you want to store the downloaded blacklist.
# Make the script executable: chmod +x update_rpz_blacklist.sh
# Schedule the script using cron, if you want it to run daily at 2 AM: crontab -e
# Add the following line (except for #) at the end of the file (make sure to replace `/path/to/script/` with the actual directory where your script is located):
# 0 2 * * * /path/to/script/update_rpz_blacklist.sh
# Save and exit. The script will now run every day at 2 AM, updating the RPZ blacklist and reloading BIND.

# Directory to store the downloaded blacklist
DIRECTORY="/path/to/store/rpz_blacklist"

# URL to the RPZ blacklist
BLACKLIST_URL="https://github.com/fabriziosalmi/blacklists/raw/main/rpz_blacklist.tar.gz"

# Ensure the directory exists
mkdir -p $DIRECTORY

# Download the latest RPZ blacklist from the repository
wget -O $DIRECTORY/rpz_blacklist.tar.gz "$BLACKLIST_URL"

# Extract the blacklist
tar -xzf $DIRECTORY/rpz_blacklist.tar.gz -C $DIRECTORY

# Check if the configuration is already added to avoid duplicate entries
if ! grep -q "rpz.blacklist" /etc/bind/named.conf.local; then
    # Append configuration to BIND's config file
    echo "zone \"rpz.blacklist\" {
    type master;
    file \"$DIRECTORY/rpz_blacklist.txt\";
};" >> /etc/bind/named.conf.local

    echo "options {
    response-policy { zone \"rpz.blacklist\"; };
};" >> /etc/bind/named.conf.local
fi
