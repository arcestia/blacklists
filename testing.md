## TODO ASAP
- ~~Create Release for RPZ blacklist and remove rpz_blacklist.tar.gz file~~
- Remove all.fqdn.blacklist.tar.gz file from repo
- Fix github pages deploy on release
- Remove old blacklists monitor (last modifier time table)
- Remove blacklists with updates older than 1d
- Improve README.md files and action and move it away from root folder
- Clean root folder
   
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
- Resolving ip addresses to fqdns (ip blacklists, CrowdSec and more) and create custom lists



