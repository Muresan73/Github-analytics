import logging
from github import Github
from git import Repo
import requests
import re
import tempfile
import os
from os import walk
import datetime
import time
import json
import pulsar

# using an access token
tokens = ['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', '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', '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']
#token = '<TOKEN>'


client = pulsar.Client('pulsar://pulsar:6650')
producer = client.create_producer('repos')
consumer = client.subscribe('dates', subscription_name='scraper')

default = False
logging.basicConfig(level=logging.INFO)


def get_repositories(date, pageNum, token):
    headers = {
        'Authorization': 'token ' + token,
        'Accept': 'application/vnd.github.v3+json'
    }
    payload={}
    # TODO: Change per_page to 100
    url = "https://api.github.com/search/repositories?q=pushed:" + str(date) + "&archived:false&page=" + str(pageNum) + "&per_page=100"
    logging.info("URL: %s" % url)
    response = requests.request("GET", url, headers=headers, data=payload)

    for item in response.json()['items']:
        language = item['language']
        cloneUrl = item['clone_url']
        fullName = item['full_name']
        # Send these 3 info to pulsar for each of the repos
        message = {"full_name": fullName,
                   "language": language,
                   "clone_url": cloneUrl}
        jsonMessage = json.dumps(message)
           
        logging.info("Sending message: %s" % jsonMessage)
        producer.send((jsonMessage).encode('utf-8'))
        #get_commits_number(item['full_name'])

''' Function to get the rate limits for each category
    The function can be used for the "round-robin"
    exchange of tokens
'''
def get_rate_limit(g):
    limit = g.get_rate_limit()
    return limit.search.remaining

def main():
    token_num = 0
    token = tokens[token_num]
    g = Github(token, per_page=10)
    pageNum = 0
    logging.info("Starting scraping of repos")
    while True:
        message = consumer.receive()
        logging.info(message)
        consumer.acknowledge(message)
        logging.info("Received message : '%s'" % message.data())

        dateInfo = json.loads(message.data().decode("utf-8"))
        pageNum = dateInfo['page']
        date = datetime.datetime.strptime(dateInfo['date'], '%d-%m-%Y')
        
        # Token handling
        remaining = get_rate_limit(g)
        logging.info("Remaining: %s" % remaining)
        if remaining <= 1:
            token_num += 1
            if token_num == 3:
                token_num = 0
            token = tokens[token_num]
            g = Github(token, per_page=10)
            remaining = get_rate_limit(g)
            if remaining <= 1:
                logging.info("Rate limit reached for all token")
                time.sleep(3600)

        get_repositories(date.date(), pageNum, token)
            
        logging.info("Finished day: %s" % date)
        
        
    client.close()


if __name__ == "__main__":
    main()

