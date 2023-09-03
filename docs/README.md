# Documentation

- [Generating the blacklist](https://github.com/fabriziosalmi/blacklists/blob/main/docs/README.md#generating-the-blacklist)
- [Downloading the blacklist](https://github.com/fabriziosalmi/blacklists/blob/main/docs/README.md#downloading-the-blacklist)
- [Implementing the blacklist](https://github.com/fabriziosalmi/blacklists/blob/main/docs/README.md#implementing-the-blacklist)
- [Integrate your whitelist]()
- [Blacklist mirror]()

## Generating the blacklist 

I leverage the power of ChangeDetection ([selfhosted](https://changedetection.io/)) to monitor and incorporate updates from selected [blacklists](https://github.com/fabriziosalmi/blacklists/blob/main/blacklists.fqdn.urls). These blacklists are downloaded hourly and aggregated into a single file: [**all.fqdn.blacklist.tar.gz**](https://github.com/fabriziosalmi/blacklists/blob/main/all.fqdn.blacklist.tar.gz) using GitHub Actions.

In addition to that I run periodic in-depth [reviews](https://github.com/fabriziosalmi/blacklists/blob/main/docs/blacklists_reviews.md) against the source blacklists and whitelist updates to ensure high quality informations.

## Downloading the Blacklist

The blacklist file is automatically updated every hour and available for downloading at the following urls: 
```
https://get.domainsblacklists.com/blacklist.txt
```

#### Alternative downloads from GitHub

- [TAR.GZ](https://fabriziosalmi.github.io/blacklists/all.fqdn.blacklist.tar.gz)
- You can clone the repo to get the [tar.gz](https://github.com/fabriziosalmi/blacklists/raw/main/all.fqdn.blacklist.tar.gz) file, I suggest to fetch latest objects only with `git clone --depth 1` command

## Implementing the Blacklist

### [PiHole](https://pi-hole.net/)
1. **Go to Adlists**
2. **Add new adlist**
```
https://get.domainsblacklists.com/blacklist.txt
```
3. **Go to Tools > Update Gravity and click the Update button**

### [AdGuard Home](https://adguard.com/it/adguard-home/overview.html)
1. **Go to Filters**
2. **Click on Add Blacklist**
3. **Add custom blacklist and save**
```
https://get.domainsblacklists.com/blacklist.txt
```

### [Squid](http://www.squid-cache.org/)

#### Squid configuration for blacklist

1. **Download and copy the blacklist to the squid folder**
```
wget -O blacklist.txt https://get.domainsblacklists.com/blacklist.txt
cp blacklist.txt /etc/squid/conf.d/blacklist.txt
```
2. **/etc/squid/squid.conf additional configuration**
```
acl blacklist dstdomain /etc/squid/conf.d/blacklist.txt     # <= blacklist location
http_access deny blacklist                                  # <= deny acl
```
3. **Restart squid**
4. **Setup a cronjob to automatically update the blacklist**

--- 

#### Squid configuration for block direct ip requests

If you're using Squid as an outgoing proxy and want to block direct IP requests (both HTTP and HTTPS) while only allowing client requests with host headers, you can achieve this by adding specific access control lists (ACLs) and http_access rules in your Squid configuration.

Here are the steps to configure Squid to achieve this:

1. **Edit the Squid Configuration File**:

Open the Squid configuration file (`squid.conf`) in a text editor:

```bash
sudo nano /etc/squid/squid.conf
```

2. **Define ACLs for Requests with Host Headers**:

Define an ACL for requests that have host headers:

```bash
acl with_host_header dstdomain . # Matches requests with a domain name
acl ip_request dstdom_regex ^\d+\.\d+\.\d+\.\d+$ # Matches requests with IP addresses
```

3. **Block Direct IP Requests**:

Now, allow requests with host headers while denying those with direct IP addresses:

```bash
http_access deny ip_request
http_access allow with_host_header
```

4. **Other Required Access Controls**:

You'll probably have other `http_access` lines in your configuration for various rules. Make sure that the order of these rules does not conflict with the rules you just added. In Squid, the first matching rule wins, so more specific rules should come before more general ones.

5. **Save and Restart Squid**:

After making these changes, save the configuration file and restart Squid to apply the changes:

```bash
sudo systemctl restart squid
```

With these changes, Squid will deny requests made directly to IP addresses and will only allow requests with host headers. Ensure you test the configuration after applying the changes to make sure it works as intended and to identify if there are any other conflicting rules.

### Linux, Windows, OSX and any device with a browser able to install the [uBlock Origin](https://github.com/gorhill/uBlock#ublock-origin) extension

1. Open the browser and go to the uBlock Origin dashboard by clicking on the extension icon > settings icon
2. Go to the end of the page and in the Import form paste this url
```
https://get.domainsblacklists.com/blacklist.txt
```
3. Click on the Apply Changes button in the top of the page
4. You will find the blacklist in the Custom list at the end of the page, before the Import form
5. You can force blacklist refresh from the same page when needed

### Linux (nftables)

!! WARNING: use at your own risk !!

1. Download [this script](https://github.com/fabriziosalmi/blacklists/blob/main/nft_blacklist_fqdn.sh) to your Linux box
2. Give permission and execute
```
chmod +x nft_blacklist_fqdn.sh && ./nft_blacklist_fqdn.sh
```

## Integrate your whitelist

You can open an issue to whitelist specific domains.

If you want to keep your whitelist secret you can use this script which use a whitelist.txt file to filter out domains from blacklist.txt file:

```
#!/bin/bash

# Remove comments and empty lines, then trim whitespace
clean_file() {
    grep -v '^#' "$1" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' | grep -v '^$'
}

# Use temporary files to store cleaned contents
clean_file blacklist.txt > /tmp/cleaned_blacklist.txt
clean_file whitelist.txt > /tmp/cleaned_whitelist.txt

# Remove domains from blacklist that are present in the whitelist
grep -vFxf /tmp/cleaned_whitelist.txt /tmp/cleaned_blacklist.txt > cleaned_blacklist.txt

# Cleanup
rm /tmp/cleaned_blacklist.txt /tmp/cleaned_whitelist.txt
```

Steps:

1. The `clean_file` function processes the input files to remove comments (lines starting with `#`), empty lines, and trims whitespace.
2. The `grep -vFxf` command is used to remove exact lines from the blacklist that match any line in the whitelist.
3. Temporary files are cleaned up at the end.

To use this script:

1. Save it as, say, `clean_blacklist.sh`.
2. Make it executable: `chmod +x clean_blacklist.sh`.
3. Run it: `./clean_blacklist.sh`.

After execution, you'll have a file named `cleaned_blacklist.txt` with the domains from the `blacklist.txt` after removing any that appear in `whitelist.txt`.

## Docker

A [Docker image](https://hub.docker.com/repository/docker/fabriziosalmi/blacklists/) is available to run a blacklist mirror on your own environment. 

- `docker pull fabriziosalmi/blacklists:latest`
- `docker run -p 80:80 fabriziosalmi/blacklists`
- The blacklist will be available at `http://$DOCKER_IP/blacklist.txt`
- To update the blacklist restart the container
