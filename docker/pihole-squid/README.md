# PiHole-Squid docker image

For more recent versions of Pi-hole, blacklisting is managed through its database (`gravity.db`). Directly modifying the database is possible, but not recommended as a general practice since there are Pi-hole CLI tools that handle this for you.

However, to get a custom list integrated, you can add the list URL to the adlist used by Pi-hole:

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

If you strictly want to automate the addition of the custom list without going through the web interface, you would have to integrate commands for that in your setup process or script, which might involve directly manipulating the `gravity.db`. This approach is more intricate and requires careful handling to ensure no data corruption occurs.

**Final step:**

1. Run `docker-compose up -d` to start both containers.
