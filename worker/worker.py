from github import Github
from git import Repo
import requests
import re
import tempfile
import os
from os import walk
import pulsar
import json
import logging
import sys
import psycopg2

p_languages = {
    'python': '(testproject|gauge|jasmin|pytest|unittest|Nose2|Testify)',
    'java': '(serenity|testproject|sahi|galen|gauge|OpenTest|karate-dsl|junit|spock|testng|dbUnit|greenmail|h2database|jmockit1|junit5|embedded-redis|mockito|restassured|android-screenshot-lib)',
    'javascript': '(cypress|testproject|sahi|galen|gauge|WebDriverIO|karate-dsl|jasmin|mocha|jest)',
    'c#': '(testproject|gauge|nunit)',
    'go': 'gauge',
    'ruby':  '(gauge|jasmin)',
    'visualbasic': 'nunit',
    'scala': '(citrus|restassured)',
    'groovy': '(citrus|spock)',
    'haskell': 'QuickCheck',
    'rust': 'test',
    'elixir': 'test',
}

default = False
logging.basicConfig(level=logging.INFO)

''' Function to get the rate limits for each category
    The function can be used for the "round-robin"
    exchange of tokens
'''
def get_rate_limit():
    limit = g.get_rate_limit()
    print("Limit for graphql:", limit.graphql)
    print("Limit for core:", limit.core)
    print("Limit for search:", limit.search)
    
''' Function to clone repositories in temp directory
'''
def clone_repo(clone_url, language, full_name):
    logging.info("Starting cloning")
    tests = False
    ci_cd = False
    with tempfile.TemporaryDirectory() as tmpdirname:
        Repo.clone_from(clone_url, tmpdirname)
        repo = Repo(tmpdirname)
        commits_count = repo.git.rev_list('--count', 'HEAD')
        logging.info('Commits count: %s' % commits_count)
        tests, ci_cd = static_analysis(tmpdirname, language)
        logging.info('Tests: %s' % tests)
        logging.info('CI/CD: %s' % ci_cd)
    database_insert(full_name, language, commits_count, tests, ci_cd)

def static_analysis(tmpdirname, language):
    logging.info("Starting static analysis")
    tests = False
    ci_cd = False
    ci_cd_list = ['.circleci', 'bamboo-specs', 'workflows', '.jenkins']
    test_reg = re.compile(".*(test|spec).*", re.IGNORECASE)
    if language in p_languages:
        langTestReg = re.compile(p_languages[language].lower(), re.IGNORECASE)

    for root, dirs, files in walk(tmpdirname):
        logging.info('Root: %s' % root)
        for dir in dirs:
            if dir in ci_cd_list:
                logging.info('Directory for ci/cd: %s' % dir)
                ci_cd = True 
            if not tests:
                for file_name in files:
                    if language in p_languages:
                        logging.info("Language: %s" %language)
                        # Case opening each file
                        # TODO: Add more types of test or do it per language
                        with open(os.path.join(root, file_name),'r') as f:
                            logging.debug('File name opened: %s' % file_name)
                            try:
                                data = f.read()
                                data = data.lower()

                                if re.match(langTestReg, data):
                                    logging.info('File for testing: %s' % file_name)
                                    tests = True
                                    break
                            except:
                                continue
                    # Case checking only the name of the file
                    else:
                        if re.match(test_reg, file_name):
                            logging.info('File name for testing: %s' % file_name)
                            tests = True
                            break
                    if '.travis.yml' in file_name:
                        ci_cd = True

            if ci_cd and tests:
                return (True, True)
    # except Exception as e:
    #     exc_type, exc_obj, exc_tb = sys.exc_info()
    #     fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #     logging.info(exc_type, fname, exc_tb.tb_lineno)
        #logging.error(e)
    logging.info('CI/CD %s' % ci_cd)
    logging.info('Tests %s' % tests)            
    return (tests, ci_cd)

#get_commits('<REPO_NAME>')
#ci_cd_tests('<REPO_NAME>')
#get_repositories()
#get_rate_limit()
#test_repo()

def database_insert(name, language, commits, tests, ci_cd):
    logging.info('Storing result to database')
    try:
        conn = psycopg2.connect(
            host="database",
            database="postgres",
            user="postgres",
            password="dbpass")

        cur = conn.cursor()

        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        sql = """INSERT INTO repository(name, language, commits, tests, ci_cd)
                VALUES(%s, %s, %s, %s, %s) RETURNING id;"""

        cur.execute(sql, (name, language, commits, tests, ci_cd,))

        # get the generated id back
        vendor_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    finally:
        if conn is not None:
            conn.close()


def main():
    client = pulsar.Client('pulsar://pulsar:6650')
    consumer = client.subscribe('repos', subscription_name='worker')

    while True:
        message = consumer.receive()
        try:
            print("Received message : '%s'" % message.data())
            
            repoInfo = json.loads(message.data().decode("utf-8"))
            
            fullName = repoInfo["full_name"]
            language = repoInfo["language"]
            cloneUrl = repoInfo["clone_url"]
            logging.info("Clone url: %s" % cloneUrl)
            
            clone_repo(cloneUrl, language, fullName)
            """ # Repo-Language mapping.
            repo_language_dict[repo_name] = language
            # Languages-Number of repos mapping.
            languages_dict[language] = languages_dict.get(language, 0) + 1
            
            # Print the progress.
            print(f"Current result: {languages_dict}") """

            # Acknowledge for receiving the message
            consumer.acknowledge(message)
        except Exception as e:
            print(e)
            consumer.negative_acknowledge(message)

    

if __name__ == "__main__":
    main()
