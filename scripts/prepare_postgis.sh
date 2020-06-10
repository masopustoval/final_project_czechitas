#!/usr/bin/bash
sudo docker network create -d bridge ruian-network
sudo docker run -d --network ruian-network --restart always --name ruian-postgis -e POSTGRES_DB=ruian -e POSTGRES_USER=ruianuser -e POSTGRES_PASSWORD=123456 postgis/postgis
