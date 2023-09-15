#!/bin/bash

echo "Setup script"

# Detect package manager
if command -v apt-get &>/dev/null; then
    PACKAGE_MANAGER="apt-get"
    UPDATE_CMD="sudo apt-get update"
    INSTALL_CMD="sudo apt-get install -y"
elif command -v apk &>/dev/null; then
    PACKAGE_MANAGER="apk"
    UPDATE_CMD="sudo apk update"
    INSTALL_CMD="sudo apk add --no-cache"
else
    echo "Unsupported package manager. Exiting."
    exit 1
fi

# Update and install prerequisites
$UPDATE_CMD
$INSTALL_CMD python3

# Link python3 to python (for Ubuntu, since Alpine doesn't have python2 by default)
if [ "$PACKAGE_MANAGER" == "apt-get" ]; then
    sudo ln -s /usr/bin/python3 /usr/bin/python
fi

python3 -m ensurepip --upgrade
pip3 install --no-cache-dir --upgrade pip setuptools tldextract tqdm

# Install pv and ncftp based on the detected package manager
for package in pv ncftp; do
    if ! $INSTALL_CMD $package; then
        echo "Failed to install '$package' using $PACKAGE_MANAGER."
        exit 1
    fi
done


LISTS="blacklists.fqdn.urls"

# Function to download a URL
download_url() {
  local url="$1"
  echo "Blacklist: $url"

  random_filename=$(uuidgen | tr -dc '[:alnum:]')

  if ! wget -q --progress=bar:force -O "$random_filename.fqdn.list" "$url"; then
    echo "Failed to download: $url"
  fi
}

echo "Download blacklists"

# Download URLs from the list
while IFS= read -r url; do
  download_url "$url"
done < "$LISTS"

FILES=$(ls *.fqdn.list)

echo "Aggregate blacklists"
echo "">aggregated.fqdn.list

while IFS= read -r file; do
  sudo cat "$file" >> aggregated.fqdn.list
done <<< "$FILES"

sudo cat aggregated.fqdn.list | sort -u > all.fqdn.blacklist
echo "Remove source files"
sudo rm ./*.fqdn.list


echo "Sanitize blacklists"
mv all.fqdn.blacklist input.txt
python sanitize.py
mv output.txt all.fqdn.blacklist

echo "Remove whitelisted domains"
mv all.fqdn.blacklist blacklist.txt
python whitelist.py
mv filtered_blacklist.txt all.fqdn.blacklist
rm blacklist.txt input.txt

total_lines_new=$(cat all.fqdn.blacklist | wc -l)
echo "Total domains: $total_lines_new."
