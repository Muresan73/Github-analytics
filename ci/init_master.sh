#!/bin/bash

add-apt-repository cloud-archive:wallaby
apt-add-repository ppa:ansible/ansible # apt update

curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

sudo docker swarm init

TOKEN=$(sudo docker swarm join-token worker -q)
IP=$(hostname -I | cut -d' ' -f1)
sed -i "s/'<token>'/$TOKEN/" default.yml
sed -i "s/'<ip>'/$IP/" default.yml

sudo apt install python3-pip nova-compute python3-openstackclient

sudo apt install ansible

sudo chown ubuntu  /etc/ansible/hosts

export OS_USER_DOMAIN_NAME="snic"
export OS_IDENTITY_API_VERSION="3"
export OS_PROJECT_DOMAIN_NAME="snic"
export OS_PROJECT_NAME="UPPMAX 2020/1-3"

source UPPMAX\ 2020_1-3-openrc.sh

# generate ssh key for start_instance
# TODO run start_instance
# TODO run ansible playbook - ansible-playbook playbook.yml