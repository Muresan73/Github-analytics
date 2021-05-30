#!/bin/bash

# Add openstack cli and ansible repo to apt
add-apt-repository cloud-archive:wallaby
apt-add-repository ppa:ansible/ansible # apt update

# Intall docker on master node
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Swith docker to swarm mode
sudo docker swarm init

# Add Swarm access token and local ip to ansible config
TOKEN=$(sudo docker swarm join-token worker -q)
IP=$(hostname -I | cut -d' ' -f1)
sed -i "s/'<token>'/$TOKEN/" ansible_config.yml
sed -i "s/'<ip>'/$IP/" ansible_config.yml

# Install openstack cli 
sudo apt install python3-pip nova-compute python3-openstackclient

# Install ansible
sudo apt install ansible

# change owner of ansible host so the local user can modify it
sudo chown $(whoami) /etc/ansible/hosts

echo '
1. configure openstack for UPPMAX
$ source UPPMAX\ 2020_1-3-openrc.sh

2. deploy worker instances
$ python3 start_Instance.py

3. configure instances with ansible
$ ansible-playbook playbook.yml
'