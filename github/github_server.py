from setup import simple_get
import sys
import json
import pprint
from datetime import datetime

pp = pprint.PrettyPrinter(depth=6)

GITHUB_V3_URL = 'https://api.github.com'
ACCESS_TOKEN = sys.argv[1]
MY_TEAM = sys.argv[2].split(',') or []

def get_my_repos(personal_token):
    """Get all repos of user

    Parameters:
        access_token (string): 

    Returns:
        repos (dict): 
        Or raising an error if http is failing

    """
    github_url = GITHUB_V3_URL + '/user/repos?per_page=100&access_token=' + personal_token
    response = simple_get(github_url)
    github_repos_as_json = json.loads(response)
    return github_repos_as_json

    # Raise an exception if we failed to get any data from the url
    raise Exception('Error retrieving contents at {}'.format(github_url))


def get_pulls_of_a_repo(repo_name, personal_token):
    """Get all repos of user

    Parameters:
        access_token (string): 

    Returns:
        repos (dict): 
        Or raising an error if http is failing

    """
    github_url = GITHUB_V3_URL + '/repos/' + repo_name + '/pulls?per_page=100&access_token=' + personal_token
    response = simple_get(github_url)
    github_pulls_as_json = json.loads(response)
    return github_pulls_as_json

    # Raise an exception if we failed to get any data from the url
    raise Exception('Error retrieving contents at {}'.format(github_url))

def get_statuses_of_a_pull(statuses_url, personal_token):
    """Get all repos of user

    Parameters:
        access_token (string): 

    Returns:
        repos (dict): 
        Or raising an error if http is failing

    """
    github_url = statuses_url + '?access_token=' + personal_token
    response = simple_get(github_url)
    github_pulls_as_json = json.loads(response)
    return github_pulls_as_json

    # Raise an exception if we failed to get any data from the url
    raise Exception('Error retrieving contents at {}'.format(github_url))



def get_github_data(personal_token):
    """

    Parameters:
        access_token (string): 

    Returns:
        repos (dict): 
        Or raising an error if http is failing

    """
    

    repos = get_my_repos(ACCESS_TOKEN)
    prs = list()
    for repo in repos: 
      pulls_in_repo = get_pulls_of_a_repo(repo["full_name"], ACCESS_TOKEN)
      for pull_request in pulls_in_repo: 
          creator = pull_request["user"]["login"]
          if creator not in MY_TEAM:
              break
          pr_data = dict()
          
          pr_data["pr_name"] = pull_request["title"] + " - " + pull_request["user"]["login"]
          pr_data["pr_url"] = pull_request["url"]
          pr_data["pr_status"] = pull_request["state"]
          pr_data["pr_updated"] = pull_request["updated_at"]
          
          pr_reviewers_names = list()
          for requested_reviewer in pull_request["requested_reviewers"]: 
              pr_reviewers_names.append(requested_reviewer['login'])
          pr_data["pr_reviewers"] = pr_reviewers_names

          pr_labels = pull_request["labels"]
          pr_labels_names = list()
          for pr_label in pr_labels: 
              pr_labels_names = pr_label['name']
          pr_data["pr_labels_names"] = pr_labels_names

          pr_statuses = get_statuses_of_a_pull(pull_request["statuses_url"], ACCESS_TOKEN)
          pr_checks_statuses = dict()
          for pr_status in pr_statuses:
              if not pr_status['context'] in pr_checks_statuses: 
                  pr_checks_statuses[pr_status['context']] = pr_status['state']
          pr_data["pr_checks_statuses"] = pr_checks_statuses
          prs.append(pr_data) 
    return prs

def print_github_data(pull_requests_data):
    """

    Parameters:
        pull_requests_data (array): all prs' data.

    Returns:
        NULL

    Side effects:
        Print all waiting prs' data

    """
    for pull_request in pull_requests_data:
        print("ֿ\n")
        print("\033[4m{}. ({}, \033[1m{}\033[0;37;40m)\033[0;37;40m".format(pull_request["pr_name"], pull_request["pr_status"], pull_request["pr_labels_names"]))
        for key,val in pull_request["pr_checks_statuses"].items():
            if val == "success":
                print("\033[92m{} V\033[0;37;40m".format(key))
            if val == "failure":
                print("\033[91m{} X\033[0;37;40m".format(key))
        then = datetime.strptime(pull_request["pr_updated"], "%Y-%m-%dT%H:%M:%SZ")
        now  = datetime.now()
        duration = now - then
        duration_in_s = duration.total_seconds()
        hours_divmod = divmod(duration_in_s, 3600)
        hours = hours_divmod[0]
        minutes = divmod(hours_divmod[1], 60)[0] 
        print("Last updated before {} hours, {} minutes. ({})".format(hours, minutes, then.strftime("%m/%d/%Y, %H:%M:%S")))
        print("Reviewers: {}".format(pull_request["pr_reviewers"]))
        print("URL: {}".format(pull_request["pr_url"]))
    return
                
prs = get_github_data(ACCESS_TOKEN)
print_github_data(prs)