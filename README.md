# Github-analytics

The repository is part of the project assignment for DE-2 Project

## Start the service

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

## Setup Grafana
In order to setup the visualisation in Grafana, the data source needs to be created and the dashboard needs to be imported.

### Port forwarding 
Since the port 3000 where Grafana is running, is not open, use port forwarding to access it locally, using:
```bash
ssh -N -f -L localhost:3000:localhost:3000 ubuntu@<SERVER_IP>
```

### Login
Login using the defaults credentials `admin:admin` and change the password.

### Add Datasource
Navigate to configuration and add a new postgres datasource with the following credentials:
- `Host: database:5432`
- `Database: postgres`
- `User: postgres`
- `Password: databasepass`
- `TLS/SSL Mode: disable`

Save and test the datasource; a green message should appear showing that the datasource was successfully added.

### Import dashboard
Press the plus button in the menu, select import and use JSON file. Select the `grafana/Main dashboard-1622293183944.json`. A dashboard named `Main dashboard` should be created, containing the queries for the 4 questions.

### Queries
The queries used in the imported Grafana dashboard are shown in the following sections. Presenting a different number of results can be achieved by changing the number of the limit.

#### Query for commits
```bash
SELECT NOW() AS "time",  name AS metric, commits as value FROM repository where LENGTH(name) > 1 ORDER BY commits desc LIMIT 10
```
#### Query for languages
```bash
SELECT NOW() AS "time",  language AS metric, count(*) as value FROM repository where LENGTH(language) > 1 GROUP BY language ORDER BY value desc LIMIT 10
```
#### Query for tests
```bash
SELECT NOW() AS "time",  language AS metric, count(*) as value FROM repository where LENGTH(language) > 1 and tests = true GROUP BY language ORDER BY value desc LIMIT 10
```
#### Query for ci/cd
```bash
SELECT NOW() AS "time",  language AS metric, count(*) as value FROM repository where LENGTH(language) > 1 and ci_cd = true GROUP BY language ORDER BY value desc LIMIT 10
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