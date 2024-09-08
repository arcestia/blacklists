#!/bin/bash

echo "Setup script 🛠️"

# Detect package manager and configure commands for package operations
detect_package_manager() {
    if command -v apt-get &>/dev/null; then
        PACKAGE_MANAGER="apt-get"
        UPDATE_CMD="sudo apt-get update"
        INSTALL_CMD="sudo apt-get install -y"
    elif command -v apk &>/dev/null; then
        PACKAGE_MANAGER="apk"
        UPDATE_CMD="sudo apk update"
        INSTALL_CMD="sudo apk add --no-cache"
    else
        echo "Unsupported package manager. Exiting ❌."
        exit 1
    fi
}

# Update and install prerequisites
update_and_install() {
    echo "Updating system and installing Python 3..."
    $UPDATE_CMD
    $INSTALL_CMD python3
    # Link python3 to python, if needed (mainly for Ubuntu systems)
    if [ "$PACKAGE_MANAGER" == "apt-get" ]; then
        sudo ln -s /usr/bin/python3 /usr/bin/python
    fi
    python3 -m ensurepip --upgrade
    pip3 install --no-cache-dir --upgrade pip setuptools tldextract tqdm
}

# Install additional required packages
install_additional_packages() {
    for package in pv ncftp; do
        if ! $INSTALL_CMD $package; then
            echo "Failed to install '$package' using $PACKAGE_MANAGER ❌."
            exit 1
        fi
    done
}

# Function to download a URL and save to a randomly named file
download_url() {
    local url="$1"
    echo "Downloading blacklist: $url"
    local random_filename=$(uuidgen | tr -dc '[:alnum:]')
    if ! wget -q --progress=bar:force -O "$random_filename.fqdn.list" "$url"; then
        echo "Failed to download: $url ❌"
    fi
}

# Download all URLs from the list and handle files
manage_downloads() {
    local LISTS="blacklists.fqdn.urls"
    echo "Starting downloads..."
    while IFS= read -r url; do
        download_url "$url"
    done < "$LISTS"
    echo "Aggregating blacklists..."
    echo "" > aggregated.fqdn.list
    for file in *.fqdn.list; do
        sudo cat "$file" >> aggregated.fqdn.list
    done
    sort -u aggregated.fqdn.list > all.fqdn.blacklist
    echo "Cleanup: removing source files..."
    sudo rm ./*.fqdn.list aggregated.fqdn.list
}

# Sanitize and whitelist downloaded blacklists
sanitize_and_whitelist() {
    echo "Sanitizing blacklists..."
    mv all.fqdn.blacklist input.txt
    python sanitize.py
    mv output.txt all.fqdn.blacklist
    echo "Removing whitelisted domains..."
    mv all.fqdn.blacklist blacklist.txt
    python whitelist.py
    mv filtered_blacklist.txt all.fqdn.blacklist
    rm blacklist.txt input.txt
}

# Main routine
main() {
    detect_package_manager
    update_and_install
    install_additional_packages
    manage_downloads
    sanitize_and_whitelist
    local total_lines_new=$(wc -l < all.fqdn.blacklist)
    echo "Total domains: $total_lines_new 🌍."
}

main
