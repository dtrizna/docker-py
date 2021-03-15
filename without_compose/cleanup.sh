#!/bin/bash

docker container rm --force triznadm-redis
docker container rm --force triznadm-http1
docker container rm --force triznadm-http2
docker container rm --force triznadm-http3
docker container rm --force triznadm-lb
docker image rm --force http-server-triznadm:1.0
docker image rm --force load-balancer-triznadm:1.0
docker container rm --force bb-triznadm
docker network rm intranet-vlan