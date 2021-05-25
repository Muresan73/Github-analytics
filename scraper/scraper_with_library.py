from github import Github
import requests
import re 
from git import Repo
import tempfile

# using an access token
token = '<YOUR_TOKEN>'
g = Github(token, per_page=10)

headers = {
    'Authorization': 'token ' + token,
    'Accept': 'application/vnd.github.v3+json'
}
payload={}

default = False

''' Function to get all the repositories based
    on the query defined in the first line
'''
def get_repositories():
    query = 'pushed:>2020-05-24 archived:false'
    repos = g.search_repositories(query, sort='stars', order='desc')
    for i in range (1):
        print(repos[i].full_name , repos[i].language)
        #get_commits(repos[i])        

''' Function to get the total number of commits'''
def get_commits(repo):
    repo = g.get_repo("PyGithub/PyGithub")
    commits = repo.get_commits()
    print(repo.full_name, commits.totalCount)

''' Function to check if the repository has tests and ci/cd
    If there exists a folder named .*test.*, then we assume
    the project has tests
    If there exists a directory for circleci or bamboo or
    github actions there exists ci/cd
    If there exits a travis.yaml there exists ci/cd
'''
def ci_cd_tests(repo):
    tests = False
    ci_cd = False
    ci_cd_list = ['.circleci', 'bamboo-specs']
    repo = g.get_repo("facebook/react")
    contents = repo.get_contents("")
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            if re.match(".*test.*", file_content.name, re.IGNORECASE):
                tests = True
            if (file_content.name in ci_cd_list ) or (file_content.name == 'workflows' and file_content.path == '.github/workflows'):
                ci_cd = True
            if tests and ci_cd:
                break
            contents.extend(repo.get_contents(file_content.path))
        else:
            if file_content.name == '.travis.yml':
                ci_cd = True
        
    print("Tests: ", tests, "ci/cd", ci_cd)

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
def clone_repo(clone_url):
    with tempfile.TemporaryDirectory() as tmpdirname:
        Repo.clone_from(clone_url, tmpdirname)
    # TODO: Run "static analysis" on the folders
    # to find if tests and ci/cd exits


#get_commits('<REPO_NAME>')
ci_cd_tests('<REPO_NAME>')
#get_repositories()
get_rate_limit()
#test_repo()