#!/bin/bash

# ----------------------
# INSTRUCTIONS
# ----------------------
# 1. Update the DIRECTORY variable to where you want to store the downloaded blacklist.
# 2. Make this script executable: chmod +x update_rpz_blacklist.sh
# 3. Optionally, schedule this script using cron to run at desired intervals.
#    For daily execution at 2 AM:
#    crontab -e
#    Add: 0 2 * * * /path/to/script/update_rpz_blacklist.sh
# 4. After running this script, BIND will be reloaded to apply the new RPZ blacklist.
# ----------------------

# Directory to store the downloaded blacklist
DIRECTORY="/path/to/store/rpz_blacklist"

# URL to the RPZ blacklist
BLACKLIST_URL="https://github.com/fabriziosalmi/blacklists/raw/main/rpz_blacklist.tar.gz"

# Ensure the directory exists
mkdir -p $DIRECTORY

# Download and extract the RPZ blacklist
wget -O $DIRECTORY/rpz_blacklist.tar.gz "$BLACKLIST_URL"
tar -xzf $DIRECTORY/rpz_blacklist.tar.gz -C $DIRECTORY

# Update BIND configuration if not already updated
if ! grep -q "rpz.blacklist" /etc/bind/named.conf.local; then
    cat <<EOL >> /etc/bind/named.conf.local
zone "rpz.blacklist" {
    type master;
    file "$DIRECTORY/rpz_blacklist.txt";
};

options {
    response-policy { zone "rpz.blacklist"; };
};
EOL
fi

# Reload BIND
sudo systemctl reload bind9
