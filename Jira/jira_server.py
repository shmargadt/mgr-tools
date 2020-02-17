from jira_setup import simple_get, set_jira_uri
import json
import pprint
import sys
pp = pprint.PrettyPrinter(depth=6)

# The URIs for resources have the following structure:
JIRA_URI = "https://<site-url>/rest/api/3/<resource-name>"
SITE_URL = sys.argv[1]

def get_jira_data(personal_key, personal_token):
    """

    Parameters:
        personal_key (string): 
        personal_token (string): 

    Returns:
        results_as_json
        Or raising an error if http is failing

    """
    jira_url = set_jira_uri(JIRA_URI, SITE_URL, 'issue/DEMO-1')
    response = simple_get(jira_url)
    results_as_json = json.loads(response)
    return results_as_json

    # Raise an exception if we failed to get any data from the url
    raise Exception('Error retrieving contents at {}'.format(jira_url))
