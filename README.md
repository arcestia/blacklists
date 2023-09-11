# Domains Blacklist

_"Building a service on top of a regularly updated blacklist can provide immense value, not only for individual internet users but also for businesses and cybersecurity professionals. Whatever service you choose to build, ensure it's user-friendly, reliable, and secure."_

![blacklist workflow](https://github.com/fabriziosalmi/blacklists/actions/workflows/generate_fqdn.yml/badge.svg)
![GitHub last commit (branch)](https://img.shields.io/github/last-commit/fabriziosalmi/blacklists/main)

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

## Why This Blacklist?

I'm passionate about digital security, and this project is a testament to that commitment. I use this blacklist daily through a series of devices (smartphone, laptop, TV, IoT), allowing me to continually test and refine it. This ensures it remains effective across a range of applications and devices.

### Quick use

Currently, the most convenient way to utilize these blacklists on desktop and laptop computers is through the [uBlock Origin](https://github.com/gorhill/uBlock#ublock-origin) browser extension. You can import the list as a custom blacklist, which allows you to override any blocked websites instantly and browse freely.

I'm also conducting tests on the iPhone using the free version of [AdGuard Pro for IOS](https://download.adguard.com/d/18672/ios-pro?exid=3ail29lmsdyc84s84c0gkosgo). I've added the blacklist as a custom list, and the performance has been quite satisfactory.

For comprehensive protection, I've set up the following configuration:

Client -> uBlock Origin Browser Extension -> Squid Proxy -> DNS Filtering via AdGuard/Pi-Hole -> Upstream DNS on a VPS with the same blacklist loaded

Sincerily the most valuable tester is my wife, a P1 Incindent is instantly raised on some failure ^_^

This setup enables me to examine various behaviors and make daily adjustments to the whole project.

### Project Aims

1. **Always Current**: Continuously updated domain and subdomain listings from reviewed sources
2. **Optimized Retrieval**: Minimize the need for external requests
3. **Infrastructure Security**: Enhance protection across your entire digital environment

#### Always Updated
This blacklist benefits from multiple sources. Custom lists added to increase the overall security. Check my blacklists [reviews](https://github.com/fabriziosalmi/blacklists/blob/main/docs/blacklists_reviews.md) for more informations. 

#### Optimized Retrieval
Fetch the entire blacklist with one simple `wget` command:
```
wget https://get.domainsblacklists.com/blacklist.txt
```

#### Boost Your Infrastructure's Security
From mobile devices to servers and applications, the DNS-level domain blocking significantly boosts security and speed. Implementing the blacklist can reduce bandwidth consumption up  to 30% based on tests across millions of requests.

For domains you prefer accessible, simply whitelist them. For instance, selectively whitelist _graph.facebook.com_ without compromising on overall security.

## [Detailed Documentation](https://github.com/fabriziosalmi/blacklists/blob/main/docs/README.md)

Please check documentation for PiHole, AdGuard Home and Squid implementations.

## Contribute

- Propose additions or removals to the blacklist
- Enhance blacklist or whitelist processing
- Dive into statistics and data analytics

## Credits

This project owes its existence to numerous dedicated blacklist creators such as:

- [Fabrice Prigent (UT1 mirror)](https://github.com/olbat/ut1-blacklists)
- [1hosts](https://badmojr.gitlab.io/1hosts/Lite/domains.txt)
- [PolishFiltersTeam](https://gitlab.com/PolishFiltersTeam/)
- [ShadowWhisperer](https://raw.githubusercontent.com/ShadowWhisperer/BlockLists/)
- [StevenBlack](https://raw.githubusercontent.com/StevenBlack/hosts/)
- [bigdargon](https://raw.githubusercontent.com/bigdargon/hostsVN/master/hosts)
- [developerdan](https://www.github.developerdan.com/)
- [firebog](https://v.firebog.net/hosts/AdguardDNS.txt)
- [hagezi](https://gitlab.com/hagezi/)
- [malware-filter](https://malware-filter.gitlab.io/)
- [phishfort](https://raw.githubusercontent.com/phishfort/phishfort-lists/master/blacklists/domains.json)
- [phishing.army](https://phishing.army/)
- [quidsup](https://gitlab.com/quidsup/)
- [DandelionSprout](https://raw.githubusercontent.com/DandelionSprout/adfilt/)
- [RPiList](https://raw.githubusercontent.com/RPiList/specials/master/Blocklisten/)
- [What-Zit-Tooya](https://github.com/What-Zit-Tooya/Ad-Block)
- [azet12](https://raw.githubusercontent.com/azet12/KADhosts)
- [cert.pl](https://hole.cert.pl)
- [mitchellkrogza](https://raw.githubusercontent.com/mitchellkrogza/Ultimate.Hosts.Blacklist)
- [o0.pages.dev](https://o0.pages.dev)
- [pgl.yoyo.org](https://pgl.yoyo.org/)
- [lightswitch05](https://raw.githubusercontent.com/lightswitch05/hosts/)
- [frogeye.fr](https://hostfiles.frogeye.fr/)
- [fruxlabs](https://rescure.fruxlabs.com/)
- [durablenapkin](https://raw.githubusercontent.com/durablenapkin/scamblocklist/)
- [digitalside.it](https://osint.digitalside.it/Threat-Intel/lists/latestdomains.txt)
- [malwareworld.com](https://malwareworld.com/)

and many more.

For a full list, check the [complete blacklists URLs](https://github.com/fabriziosalmi/blacklists/blob/main/blacklists.fqdn.urls).

## Currently testing

- [Domain blacklist checker](https://review.domainsblacklists.com/)
- Search API
```
curl -s -H "User-Agent: DomainsBlacklists" -X POST -H "Content-Type: application/json" -d "{\"domains\": [\"$DOMAIN\"]}" https://check.domainsblacklists.com/check_domain
```

- Telegram Bot blacklist checker
- Notification (Teams via webhook, e-mail, ntfy) if blacklisted
- Firefox extension site checker
- Search API Docker image
- Resolving ip addresses to fqdns (ip blacklists, CrowdSec and more)

## Roadmap

Could be nice if some missions will be achieved:

- Check the web for more blacklists to be aggregated when possible
- Whitelist content can be improved
- Adult and newly registered domains are a huge challenge to manage on separate aggregated blacklists, postponed..
- IP blacklists integration (get FQDNs from blacklisted IPs and provide a custom FQDN  list to include in the main one)
- Domain ranking insights is a topic, should be a fail and learn initiative
- Improve documentation and website UX (especially for non techie users)
- Fix and learn from everything

---
![Static Badge](https://img.shields.io/badge/DomainsBlacklists-For_a_safer_digital_experience-00ce00?style=for-the-badge)
