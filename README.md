# Domains Blacklist

_"Building a service on top of a regularly updated blacklist can provide immense value, not only for individual internet users but also for businesses and cybersecurity professionals. Whatever service you choose to build, ensure it's user-friendly, reliable, and secure."_

![GitHub last commit (branch)](https://img.shields.io/github/last-commit/fabriziosalmi/blacklists/main) [![Generate and Release](https://github.com/fabriziosalmi/blacklists/actions/workflows/generate-and-release.yml/badge.svg)](https://github.com/fabriziosalmi/blacklists/actions/workflows/generate-and-release.yml)  [![Blacklists Monitor](https://github.com/fabriziosalmi/blacklists/actions/workflows/changedetection.yml/badge.svg)](https://github.com/fabriziosalmi/blacklists/actions/workflows/changedetection.yml) ![Uptime Robot status](https://img.shields.io/uptimerobot/status/m795278126-d795cc268595633d462de235?label=Whitelisting%20request%20service)

![Uptime Robot status](https://img.shields.io/uptimerobot/status/m795276181-ea44caeb6a6db48fdc262ac6?label=website) ![Static Badge](https://img.shields.io/badge/blacklists-60-000000) ![Static Badge](https://img.shields.io/badge/blacklisted-3653483-cc0000) ![Static Badge](https://img.shields.io/badge/whitelisted-2177-00CC00) ![Static Badge](https://img.shields.io/badge/custom_blacklisted-546-000000) ![GitHub all releases](https://img.shields.io/github/downloads/fabriziosalmi/blacklists/total) ![GitHub issues](https://img.shields.io/github/issues/fabriziosalmi/blacklists)
## Access the Blacklist

**[DOWNLOAD](https://github.com/fabriziosalmi/blacklists/releases/download/latest/blacklist.txt)** or use this up-to-the-minute blacklist as your source:

### Quick Access

```
https://get.domainsblacklists.com/blacklist.txt
```
or
```
https://github.com/fabriziosalmi/blacklists/releases/download/latest/blacklist.txt
```
### Compatibility
Works seamlessly with:
- Windows, Mac, Linux via the [uBlock Origin](https://github.com/gorhill/uBlock#ublock-origin) browser extension
- IPhone (Safari + DNS) via [AdGuard Pro for IOS](https://download.adguard.com/d/18672/ios-pro?exid=3ail29lmsdyc84s84c0gkosgo)
- Android via [AdGuard Pro for Android](https://adguard.com/it/adguard-android/overview.html)
- [PiHole](https://pi-hole.net/) and [AdGuard Home](https://adguard.com/it/adguard-home/overview.html) DNS filtering applications
- [Squid](http://www.squid-cache.org/) proxy
- Firewalls like [nftables](https://github.com/fabriziosalmi/blacklists/blob/main/scripts/nft_blacklist_fqdn.sh) and WAF like [OPNsense](https://docs.opnsense.org/manual/how-tos/proxywebfilter.html)
- DNS servers like [BIND9](https://github.com/fabriziosalmi/blacklists/tree/main/docs#how-to-implement-the-rpz-blacklist-with-bind9)
  
### Features
- **Hourly Updates**: Stay protected against emerging threats
- **Comprehensive Coverage**: Aggregated from the most frequently updated blacklists ([more info](https://github.com/fabriziosalmi/blacklists/blob/main/docs/blacklists_reviews.md))
- **Broad Compatibility**: Works across browsers, firewalls, proxies, and more
- **Robust Security**: Protect against phishing, spam, scams, ads, trackers, bad websites and more
- **Whitelist Capability**: Have more control over what you allow
- **Local Mirror**: Set up easily using the [Docker image](https://hub.docker.com/repository/docker/fabriziosalmi/blacklists/)

### Whitelist submissions

- **[Submit one or more domains for whitelisting](https://req.domainsblacklists.com/)**
## Why Use This Blacklist?

I'm deeply committed to digital security, and this blacklist reflects that commitment. I use it daily across various devices to continually test and improve its effectiveness.

**How to Use**

- On desktop and laptop computers, easily use it with the uBlock Origin browser extension. Import it as a custom blacklist for instant website unblocking
- On iPhones, it works well with AdGuard Pro for iOS as a custom list
- My setup involves a series of layers for robust protection (uBlock Origin browser extension, PiHole, AdGuard Home as PiHole upstream, Squid proxy)

**Efficient Retrieval**

Fetch the entire blacklist with a simple command:

```
wget https://get.domainsblacklists.com/blacklist.txt
```

**Enhanced Security**

Implementing DNS-level domain blocking improves security and can reduce bandwidth consumption by up to 30%. You can also selectively whitelist domains without compromising overall security.

## [Documentation](https://github.com/fabriziosalmi/blacklists/blob/main/docs/README.md)

Please check [documentation](https://github.com/fabriziosalmi/blacklists/blob/main/docs/README.md) for PiHole, AdGuard Home and Squid implementations.
## Contribute

- Propose additions or removals to the blacklist
- Enhance blacklist or whitelist processing
- Dive into statistics and data analytics
## Credits

This project owes its existence to numerous dedicated blacklist creators such as:

[T145/BlackMirror](https://github.com/T145/black-mirror) - [Fabrice Prigent (UT1 mirror)](https://github.com/olbat/ut1-blacklists) - [1hosts](https://badmojr.gitlab.io/1hosts/Lite/domains.txt) - [PolishFiltersTeam](https://gitlab.com/PolishFiltersTeam/) - [ShadowWhisperer](https://raw.githubusercontent.com/ShadowWhisperer/BlockLists/) - [StevenBlack](https://raw.githubusercontent.com/StevenBlack/hosts/) - [bigdargon](https://raw.githubusercontent.com/bigdargon/hostsVN/master/hosts) - [developerdan](https://www.github.developerdan.com/) - [firebog](https://v.firebog.net/hosts/AdguardDNS.txt) - [hagezi](https://gitlab.com/hagezi/) - [malware-filter](https://malware-filter.gitlab.io/) - [phishfort](https://raw.githubusercontent.com/phishfort/phishfort-lists/master/blacklists/domains.json) - [phishing.army](https://phishing.army/) - [quidsup](https://gitlab.com/quidsup/) - [DandelionSprout](https://raw.githubusercontent.com/DandelionSprout/adfilt/) - [RPiList](https://raw.githubusercontent.com/RPiList/specials/master/Blocklisten/) - [What-Zit-Tooya](https://github.com/What-Zit-Tooya/Ad-Block) - [azet12](https://raw.githubusercontent.com/azet12/KADhosts) - [cert.pl](https://hole.cert.pl) - [mitchellkrogza](https://raw.githubusercontent.com/mitchellkrogza/Ultimate.Hosts.Blacklist) - [o0.pages.dev](https://o0.pages.dev) - [pgl.yoyo.org](https://pgl.yoyo.org/) - [lightswitch05](https://raw.githubusercontent.com/lightswitch05/hosts/) - [frogeye.fr](https://hostfiles.frogeye.fr/) - [fruxlabs](https://rescure.fruxlabs.com/) - [durablenapkin](https://raw.githubusercontent.com/durablenapkin/scamblocklist/) - [digitalside.it](https://osint.digitalside.it/Threat-Intel/lists/latestdomains.txt) - [malwareworld.com](https://malwareworld.com/)

and many more.

For a full list, check the [complete blacklists URLs](https://github.com/fabriziosalmi/blacklists/blob/main/blacklists.fqdn.urls).
## Beta testing

- [Domain blacklist checker](https://review.domainsblacklists.com/)
- [ChangeDetection via GitHub Action](https://github.com/fabriziosalmi/blacklists/blob/main/docs/blacklists_reviews.md) (24h max)
- Search API

**example for whitelisted or non-blacklisted domain**
```
curl -s -H "User-Agent: DomainsBlacklists" -X POST -H "Content-Type: application/json" -d "{\"domains\": [\"whitelisted-or-not-blacklisted.com\"]}" https://check.domainsblacklists.com/check_domain
```

**example for blacklisted domain**
```
curl -s -H "User-Agent: DomainsBlacklists" -X POST -H "Content-Type: application/json" -d "{\"domains\": [\"ads.google.com\"]}" https://check.domainsblacklists.com/check_domain
```
  
## Alpha testing

- Telegram Bot blacklist checker
- Notification (Teams via webhook, e-mail, ntfy) if blacklisted
- Firefox extension site checker
- Search API Docker image
- Resolving ip addresses to fqdns (ip blacklists, CrowdSec and more)

#### Search API
  

## Roadmap

2023
- Improve repository (example: release only no tar.gz versioned, Pages duties)
- Improve documentation
- Improve websites
- Improve blacklist
- Improve whitelist


2024
- IP blacklists integration (get FQDNs from blacklisted IPs and provide a custom FQDN  list to include in the main one)
- Domain ranking service
- Safe browsing service
- Adult domains list
- Newly registered domains list



---
![Static Badge](https://img.shields.io/badge/DomainsBlacklists-For_a_safer_digital_experience-00ce00?style=for-the-badge)
