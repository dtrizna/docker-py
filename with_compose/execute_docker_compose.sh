#!/bin/bash

# kill any process if listens on TCP 80
netstat -ntlp | grep 80 | awk '{print $7}' | cut -d/ -f1 | xargs kill -9

# set up correct version of docker-compose
# NOTE: curl won't download the same file if already exists thanks to "-C -"
curl -C - -L https://github.com/docker/compose/releases/download/1.28.4/docker-compose-Linux-x86_64 -o /usr/bin/docker-compose
chmod +x /usr/bin/docker-compose

# build containers & images from docker-compose.yml
# force reconstruction of all componenets
/usr/bin/docker-compose up -d --force-recreate --build

# show which containers are running
docker ps

echo -e "[+] Factorial logic available via http://localhost"
echo -e "[!] Please wait ~10s for Redis to load the data before asking for factorial!"