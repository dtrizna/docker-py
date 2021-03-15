#!/bin/bash

log () {
    python3 -c "print('='*64)"
    echo -e "\n$1\n"
    python3 -c "print('='*64)"
}

log "[*] Cleanup from potential container conflicts..."
bash cleanup.sh 

# Stage 1.B

docker network create intranet-vlan

log "[*] Starting Redis container..."

docker run -d --name triznadm-redis -p 26379:6379 -v /var/cec/redis.rdb:/data/dump.rdb redis:latest
docker network connect intranet-vlan triznadm-redis

log "[+] Redis container started! Available via tcp://localhost:26379"
netstat -ntlp | grep 26379

# Stage 1.C
log "[*] Building HTTP server container..."

docker image build -t http-server-triznadm:1.0 ../http-server-docker/

for i in $(seq 1 3); do
    log "[*] Starting HTTP server container Nr.$i..."

    docker run -d -p 888$i:80 --name triznadm-http$i http-server-triznadm:1.0
    docker network connect intranet-vlan triznadm-http$i
    
    log "[+] HTTP server Nr.$i available via http://localhost:888$i "
done

# Step 1.D

log "[*] Building and Starting Load Balancing container..."

docker image build -t load-balancer-triznadm:1.0 ../load-balancer-docker/
docker run -d -p 80:80 --name triznadm-lb load-balancer-triznadm:1.0
docker network connect intranet-vlan triznadm-lb

log "[+] You can access factorial logic via http://localhost"
log "[!] Note! Yoy might need to wait ~5s for Redis to load data."
log "[!] To remove all the docker configuration, use cleanup.sh"