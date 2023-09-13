## Currently testing

- [Domain blacklist checker](https://review.domainsblacklists.com/)
- Telegram Bot blacklist checker
- Notification (Teams via webhook, e-mail, ntfy) if blacklisted
- Firefox extension site checker
- Search API Docker image
- Resolving ip addresses to fqdns (ip blacklists, CrowdSec and more)

#### Search API

  
**example for whitelisted or non-blacklisted domain**
```
curl -s -H "User-Agent: DomainsBlacklists" -X POST -H "Content-Type: application/json" -d "{\"domains\": [\"whitelisted-or-not-blacklisted.com\"]}" https://check.domainsblacklists.com/check_domain
```

**example for blacklisted domain**
```
curl -s -H "User-Agent: DomainsBlacklists" -X POST -H "Content-Type: application/json" -d "{\"domains\": [\"ads.google.com\"]}" https://check.domainsblacklists.com/check_domain
```
