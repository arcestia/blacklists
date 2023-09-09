# PiHole-Squid docker image

## How to use

1. Clone the repo and cd to this folder
2. Run `docker-compose up -d` to start both containers
3. Setup your client to use PiHole DNS service (UDP 53)
4. Setup your client to use Squid proxy (TCP 3128)

To get a custom list integrated, you can add the list URL to the adlist used by Pi-hole:
1. **Add the custom list to Pi-hole's adlists.**

Login to the Pi-hole admin console:
- Go to `Group Management` -> `Adlists`.
- Add `https://get.domainsblacklists.com/blacklist.txt` as a new list.

2. **Update Gravity Daily**

To update Pi-hole's blocklists daily (which is essentially running `pihole -g` daily):

```bash
echo "0 0 * * * root /usr/local/bin/pihole -g" | sudo tee -a /etc/cron.d/pihole
```

This cron job will cause Pi-hole to update its blocklists daily at midnight.
