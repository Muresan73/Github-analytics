#!/bin/bash

sudo docker build --network=host -t github-analytics-database ./database
sudo docker tag github-analytics-database  master:5000/github-analytics-database
sudo docker push master:5000/github-analytics-database

sudo docker build --network=host -t github-analytics-scraper ./scraper
sudo docker tag github-analytics-scraper  master:5000/github-analytics-scraper
sudo docker push master:5000/github-analytics-scraper

sudo docker build --network=host -t github-analytics-worker ./worker
sudo docker tag github-analytics-worker  master:5000/github-analytics-worker
sudo docker push master:5000/github-analytics-worker

sudo docker build --network=host -t github-analytics-initiator ./initiator
sudo docker tag github-analytics-initiator  master:5000/github-analytics-initiator
sudo docker push master:5000/github-analytics-initiator

sudo docker build --network=host -t github-analytics-test ./test
sudo docker tag github-analytics-test  master:5000/github-analytics-test
sudo docker push master:5000/github-analytics-test
