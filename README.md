# Github-analytics

The repository is part of the project assignment for DE-2 Project

## Start the serive

### Setup

- run `init_master.sh` in the ci folder
```bash
cd ci
./init_master.sh
```
- configure openstack for UPPMAX
```bash
source UPPMAX\ 2020_1-3-openrc.sh
```

- deploy worker instances
```bash
python3 start_Instance.py
```

- configure instances with ansible
```bash
ansible-playbook playbook.yml
```

### Deploy services 

- push images to local image repository
```bash
./buildImages.sh
```

- deploy swarm stack
```bash
docker stack deploy -c g19-stack.yaml ga
```

## Manual setup

#### Run local image registry
```bash
sudo docker run -d -p 5000:5000 --restart=always --name registry registry:2
```


#### Push image to registry
- add master ip to /etc/hosts 
- add to /etc/docker/daemon.json 
```json
{
    "insecure-registries" : ["master:5000"]
}
```

```bash
sudo docker build --network=host -t github-analytics .
sudo docker tag github-analytics  master:5000/github-analytics
sudo docker push master:5000/github-analytics
```


# debug

docker service ps --no-trunc
docker swarm join-token worker