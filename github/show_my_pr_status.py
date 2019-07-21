from setup import simple_get
import sys
import json
import pprint

pp = pprint.PrettyPrinter(depth=6)

GITHUB_V3_URL = 'https://api.github.com'
CLIENT_ID = sys.argv[1] 
CLIENT_SECRET = sys.argv[2] 

def get_my_repos(personal_key, personal_token):
    """Get all repos of user

    Parameters:
        client_id (string): 
        client_secret (string): 

    Returns:
        repos (dict): 
        Or raising an error if http is failing

    """
    github_url = GITHUB_V3_URL + '/user/repos?client_id=' + CLIENT_ID + '&client_secret=' + CLIENT_SECRET
    print(github_url)
    response = simple_get(github_url)
    print(response)
    return response

    # Raise an exception if we failed to get any data from the url
    raise Exception('Error retrieving contents at {}'.format(trello_url))

get_my_repos(CLIENT_ID, CLIENT_SECRET)