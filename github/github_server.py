from setup import simple_get
import sys
import json
import pprint
from datetime import datetime

pp = pprint.PrettyPrinter(depth=6)

GITHUB_V3_URL = 'https://api.github.com'
class TextColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    NORMAL = '\033[0;37;40m'

def get_my_repos(personal_token):
    """Get all repos of user

    Parameters:
        personal_token (string): access token from github

    Returns:
        github_repos_as_json (dict): dictionary of 100 recent repos in github of the user
        Or raising an error if http is failing

    """
    github_url = GITHUB_V3_URL + '/user/repos?per_page=100'
    response = simple_get(github_url, personal_token)
    github_repos_as_json = json.loads(response)
    return github_repos_as_json

    # Raise an exception if we failed to get any data from the url
    raise Exception('Error retrieving contents at {}'.format(github_url))


def get_pulls_of_a_repo(repo_name, personal_token):
    """Get all pulls of specific repository

    Parameters:
        repo_name (string): name of the relevant repository
        personal_token (string): access token from github

    Returns:
        github_pulls_as_json (dict): dictionary of 100 recent pull requests of specific repository
        Or raising an error if http is failing

    """
    github_url = GITHUB_V3_URL + '/repos/' + repo_name + '/pulls?per_page=100&direction=desc'
    response = simple_get(github_url, personal_token)
    github_pulls_as_json = json.loads(response)
    return github_pulls_as_json

    # Raise an exception if we failed to get any data from the url
    raise Exception('Error retrieving contents at {}'.format(github_url))

def get_statuses_of_a_pull(statuses_url, personal_token):
    """Get all checks statuses of a pull request

    Parameters:
        statuses_url (string): Github url for checks statuses of a pull
        personal_token (string): access token from github

    Returns:
        statuses_of_a_pull_as_json (dict): dictionary of all checks statuses of a pull request
        Or raising an error if http is failing

    """
    github_url = statuses_url
    response = simple_get(github_url, personal_token)
    statuses_of_a_pull_as_json = json.loads(response)
    return statuses_of_a_pull_as_json

    # Raise an exception if we failed to get any data from the url
    raise Exception('Error retrieving contents at {}'.format(github_url))


def get_approved_prs_of_a_repo(repo_name, personal_token):
    """

    Parameters:
        repo_name (string): The repository name of the pull requests
        personal_token (string): access token from github

    Returns:
        approved_prs_of_a_repo_as_json (dict): dictionary of all approved pull requests
        Or raising an error if http is failing

    """
    github_url = GITHUB_V3_URL + '/search/issues?q=is:open+is:pr+review:approved+repo:' + repo_name
    response = simple_get(github_url, personal_token)
    approved_prs_of_a_repo_as_json = json.loads(response) if response else []
    return approved_prs_of_a_repo_as_json

    # Raise an exception if we failed to get any data from the url
    raise Exception('Error retrieving contents at {}'.format(github_url))



def get_github_data(personal_token, my_team):
    """Gel all Github data from all repositories

    Parameters:
        personal_token (string): access token from github

    Returns:
        prs (dict): all relevant pull requests from all avaiable repositories with useful data
        Or raising an error if http is failing

    """
    

    repos = get_my_repos(personal_token)
    prs = list()
    for repo in repos:
      pulls_in_repo = get_pulls_of_a_repo(repo["full_name"], personal_token)
      approved_prs = get_approved_prs_of_a_repo(repo["full_name"], personal_token)
      approved_prs_numbers = list()
      if approved_prs and approved_prs["items"]:
        for apr_item in approved_prs["items"]:
            approved_prs_numbers.append(apr_item["number"])
      for pull_request in pulls_in_repo: 
          creator = pull_request["user"]["login"]
          if creator not in my_team:
              break

          pr_data = dict()
          
          pr_data["pr_name"] = pull_request["title"] + " - " + creator
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

          pr_statuses = get_statuses_of_a_pull(pull_request["statuses_url"], personal_token)
          pr_checks_statuses = dict()
          for pr_status in pr_statuses:
              if not pr_status['context'] in pr_checks_statuses: 
                  pr_checks_statuses[pr_status['context']] = pr_status['state']
          pr_data["pr_checks_statuses"] = pr_checks_statuses
          pr_data["pr_approved"] = pull_request["number"] in approved_prs_numbers
          prs.append(pr_data)

    return prs


def get_gap_of_hours_n_minutes(earlier_date):
    now  = datetime.now()
    duration = now - earlier_date
    duration_in_s = duration.total_seconds()
    hours_divmod = divmod(duration_in_s, 3600)
    gap_obj = dict()
    gap_obj["hours"] = hours_divmod[0]
    gap_obj["minutes"] = divmod(hours_divmod[1], 60)[0]
    return gap_obj

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
        print("{}{}. ({}){}".format(TextColors.UNDERLINE, pull_request["pr_name"], pull_request["pr_status"], TextColors.NORMAL))
        print("{}{}{}".format(TextColors.WARNING, pull_request["pr_labels_names"], TextColors.NORMAL))
        if pull_request["pr_approved"]:
            print("{}Approved: {}{}".format(TextColors.OKGREEN, pull_request["pr_approved"], TextColors.NORMAL))
        else:
            print("{}Approved: {}{}".format(TextColors.FAIL, pull_request["pr_approved"], TextColors.NORMAL))
        for key,val in pull_request["pr_checks_statuses"].items():
            if val == "success":
                print("{}{} V{}".format(TextColors.OKGREEN, key, TextColors.NORMAL))
            if val == "failure":
                print("{}{} X{}".format(TextColors.FAIL, key, TextColors.NORMAL))
        then = datetime.strptime(pull_request["pr_updated"], "%Y-%m-%dT%H:%M:%SZ")
        gap_obj = get_gap_of_hours_n_minutes(then)
        print("Last updated before {} hours, {} minutes. ({})".format(gap_obj["hours"], gap_obj["minutes"], then.strftime("%m/%d/%Y, %H:%M:%S")))
        print("Reviewers: {}".format(pull_request["pr_reviewers"]))
        print("URL: {}".format(pull_request["pr_url"]))
    return

def get_files_change_of_a_pr(repo_name, pr, personal_token):
    """Get all files change of specific pull request

    Parameters:
        repo_name (string): name of the relevant repository
        personal_token (string): access token from github

    Returns:
        github_files_as_json (dict): dictionary of 100 recent pull requests of specific repository
        Or raising an error if http is failing

    """

    github_url = GITHUB_V3_URL + '/repos/' + repo_name + '/pulls/' + str(pr['number']) + '/files?access_token=' + personal_token
    response = simple_get(github_url, personal_token)
    github_files_as_json = json.loads(response)
    return github_files_as_json

def get_merged_pulls_of_a_repo(repo_name, personal_token):
    """

    Parameters:
        repo_name (string): The repository name of the pull requests
        personal_token (string): access token from github

    Returns:
        approved_prs_of_a_repo_as_json (dict): dictionary of all approved pull requests
        Or raising an error if http is failing

    """
    github_url = GITHUB_V3_URL + '/search/issues?q=is:pr+is:merged+repo:' + repo_name + '&access_token=' + personal_token
    response = simple_get(github_url, personal_token)
    approved_prs_of_a_repo_as_json = json.loads(response) if response else []
    return approved_prs_of_a_repo_as_json

    # Raise an exception if we failed to get any data from the url
    raise Exception('Error retrieving contents at {}'.format(github_url))

def print_files_change_of_pr(repo_full_name, personal_token, pulls_in_repo):
    for pull_request in pulls_in_repo:
        then = datetime.strptime(pull_request["updated_at"], "%Y-%m-%dT%H:%M:%SZ")
        now  = datetime.now()
        duration = now - then
        week_in_seconds = 604800
        if duration.total_seconds() < week_in_seconds:
            creator = pull_request["user"]["login"]
            print("{}{} / {}. ({}) {}".format(TextColors.WARNING, pull_request['title'], creator, then.strftime("%Y-%m-%d"), TextColors.NORMAL))
            print("{}".format(pull_request["html_url"]))
            pr_files = get_files_change_of_a_pr(repo_full_name, pull_request, personal_token)
            if pr_files:
                files_changed = list()                
                for pr_file in pr_files:
                    if pr_file['filename'].find('src/') != -1: 
                        files_changed.append(pr_file['filename'])
            pp.pprint(files_changed)
    return

def get_github_repo_summary(personal_token, repo_full_name):
    pending_pulls_in_repo = get_pulls_of_a_repo(repo_full_name, personal_token)
    merged_pulls_in_repo = get_merged_pulls_of_a_repo(repo_full_name, personal_token)
    # updated_at use for update
    print("{}{}{}".format(TextColors.HEADER, "Last week changes", TextColors.NORMAL))
    print_files_change_of_pr(repo_full_name, personal_token, merged_pulls_in_repo["items"])
    print("{}{}{}".format(TextColors.HEADER, "Pending review", TextColors.NORMAL))
    print_files_change_of_pr(repo_full_name, personal_token, pending_pulls_in_repo)
    # pp.pprint(pending_pulls_in_repo[0])
    # pp.pprint(merged_pulls_in_repo["items"][0]["updated_at"])
    return merged_pulls_in_repo

def print_repo_summary(pulls_in_repo):
    # pp.pprint(pulls_in_repo)
    return