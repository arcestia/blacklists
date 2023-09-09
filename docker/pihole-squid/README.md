## pihole-squid docker image

All-In-one filtering proxy-dns (still testing, use with caution..)

**Daily Pi-hole blacklist update**

Pi-hole itself doesn't readily support fetching external blacklists daily without modifying its internal workings. However, you can still use the cron mechanism.

Inside the pihole container, run:

```bash
docker exec -it pihole_container_name /bin/bash
```

Then, add a daily cron job:

```bash
echo "0 0 * * * wget -O /etc/pihole/blacklist.txt https://get.domainsblacklists.com/blacklist.txt && pihole restartdns" | crontab -
```

Remember to replace `pihole_container_name` with the actual name of the pihole container you get from `docker ps`.

**Final steps:**

1. Adjust the `squid.conf` as per your requirements and place it inside the `squid` directory.
2. Run `docker-compose up -d` to start both containers.
