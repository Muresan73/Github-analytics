#!/bin/bash

curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

sudo docker swarm init
TOKEN=$(sudo docker swarm join-token worker -q)

sed -i "s/''/$TOKEN/" default.yml

sudo apt install python3-pip
pip install ansible