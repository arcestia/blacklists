## Why This Blacklist?

I'm passionate about digital security, and this project is a testament to that commitment. I use this blacklist daily through a series of devices (smartphone, laptop, TV, IoT), allowing me to continually test and refine it. This ensures it remains effective across a range of applications and devices.

### Quick use

Currently, the most convenient way to utilize these blacklists on desktop and laptop computers is through the [uBlock Origin](https://github.com/gorhill/uBlock#ublock-origin) browser extension. You can import the list as a custom blacklist, which allows you to override any blocked websites instantly and browse freely. If you have a good whitelist please share such domains [here](https://req.domainsblacklists.com/) to improve the project.

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
