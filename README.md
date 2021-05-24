# Github-analytics

The repository is part of the project assignment for DE-2 Project

## To start the service run

#### On master node

```bash
docker swarm init
```

```bash
docker stack deploy -c g19-stack.yaml demo
```

#### Run local image registry
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
