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
token = '<TOKEN>'
g = Github(token, per_page=10)

client = pulsar.Client('pulsar://pulsar:6650')
producer = client.create_producer('my-topic')


default = False
logging.basicConfig(level=logging.INFO)

''' Function to get all the repositories based
    on the query defined in the first line
'''
""" def get_repositories_library():
    query = 'updated_at:>2020-01-01&page=1&per_page=100'
    query = 'pushed:>2020-05-24 archived:false'
    repos = g.search_repositories(query, sort='stars', order='desc')
    for i in range (1):
        print(repos[i])
        print(repos[i].full_name , repos[i].language)
        #get_commits(repos[i].full_name) """

def get_repositories(date, pageNum, token):
    headers = {
        'Authorization': 'token ' + token,
        'Accept': 'application/vnd.github.v3+json'
    }
    payload={}
    # TODO: Change per_page to 100
    url = "https://api.github.com/search/repositories?q=pushed:" + str(date) + "&archived:false&page=" + str(pageNum) + "&per_page=100"
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
def get_rate_limit():
    limit = g.get_rate_limit()
    return limit.search.remaining

#get_commits('<REPO_NAME>')
#ci_cd_tests('<REPO_NAME>')
#get_repositories()
#get_rate_limit()
#test_repo()
#clone_repo('https://github.com/PyGithub/PyGithub.git')


""" def main():
    date = datetime.date(2020, 1 ,1)
    pageNum = 0
    while True:
        if pageNum < 10:
            logging.info('Date')
            pageNum += 1
        else: 
            date = date + datetime.timedelta(days=1)
            pageNum = 1
        # TODO: REMOVE
        #if date.day == 10:
        #    break
        remaining = get_rate_limit()
        print("Remaining: ", remaining)
        # TODO: Define three tokens
        if remaining <= 1:
            print("Rate limit reached for token")
            time.sleep(3600)

        get_repositories(date, pageNum, token)
        time.sleep(20)
    print("Broke ;)")
    client.close() """

def main():
    date = datetime.date(2020, 1 ,1)
    logging.info("Starting the service with date: %s" % date)
    pageNum = 0
    while True:
        for pageNum in range(1, 11):
            remaining = get_rate_limit()
            logging.info("Remaining: %s" % remaining)
            if remaining <= 1:
                logging.info("Rate limit reached for token")
                time.sleep(3600)

            get_repositories(date, pageNum, token)
            
        logging.info("Finished day: %s" % date)
        time.sleep(20)
        date = date + datetime.timedelta(days=1)

        # TODO: REMOVE
        """ if date.day == 10:
            break  """
        
    #print("Broke ;)")
    client.close()


if __name__ == "__main__":
    main()