from setup import simple_get
import sys
import json
import pprint

pp = pprint.PrettyPrinter(depth=6)

GITHUB_V3_URL = 'https://api.github.com'
ACCESS_TOKEN = sys.argv[1]
def get_my_repos(personal_token):
    """Get all repos of user

    Parameters:
        client_id (string): 
        client_secret (string): 

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
        client_id (string): 
        client_secret (string): 

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
        client_id (string): 
        client_secret (string): 

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

repos = get_my_repos(ACCESS_TOKEN)
pulls_in_repo = get_pulls_of_a_repo(repos[29]["full_name"], ACCESS_TOKEN)
# for pull_request in pulls_in_repo: 
#     creator = pull_request["user"]["login"]
#     if creator in ['ronysh']:
#         pp.pprint(pull_request['title'] + ", state: " + pull_request['state'])
specific_pull = pulls_in_repo[1]
pr_statuses = get_statuses_of_a_pull(specific_pull["statuses_url"], ACCESS_TOKEN)

# pulls_in_repo = get_pulls_of_a_repo(repos[3]["full_name"], ACCESS_TOKEN)
# pp.pprint(pulls_in_repo[0])
pp.pprint(specific_pull["title"] + " - " + specific_pull["user"]["login"])
pp.pprint(specific_pull["url"])
pp.pprint(specific_pull["updated_at"])
requested_reviewers = specific_pull["requested_reviewers"]
pp.pprint("reviewers:")
for requested_reviewer in requested_reviewers: 
    pp.pprint(requested_reviewer['login'])

pr_labels = specific_pull["labels"]
pp.pprint("labels:")
for pr_label in pr_labels: 
    pp.pprint(pr_label['name'])
pp.pprint(specific_pull["statuses_url"])

for pr_status in pr_statuses: 
    pp.pprint(pr_status['context'] + ", state: " + pr_status['state'] + ", created_at:" + pr_status['created_at'])
# for pull_request in pulls_in_repo: 
#     pp.pprint(pull_request['title'] + ", state: " + pull_request['state'])