#!/bin/bash

# Add openstack cli and ansible repo to apt
sudo add-apt-repository cloud-archive:wallaby
sudo apt-add-repository ppa:ansible/ansible # apt update

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
sudo apt install python3-pip nova-compute python3-openstackclient -y

# Install ansible
sudo apt install ansible -y

# change owner of ansible host so the local user can modify it
sudo chown $(whoami) /etc/ansible/hosts

sudo docker run -d -p 5000:5000 --restart=always --name registry registry:2

echo '
1. configure openstack for UPPMAX
$ source UPPMAX\ 2020_1-3-openrc.sh

2. generate ssh-key pair and add the public one to UPPMAX

3. deploy worker instances
$ python3 start_Instance.py

4. configure instances with ansible
$ ansible-playbook playbook.yml
'