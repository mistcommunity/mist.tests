#!/usr/bin/env bash
CID=$(docker ps |grep api_|cut -d " " -f1)
DOCKER_NETWORK=$(docker ps --format "{{.ID}} {{.Networks}}"|grep $CID|cut -d ' ' -f2)
docker run -p 5900:5900 -p 8222:8222 --rm -it \
	-v `pwd`:/mist.tests \
	--shm-size=1g \
	--network=$DOCKER_NETWORK \
	-e VNC=$VNC \
	mistio/tests /bin/bash
