from requests import get
from requests.exceptions import RequestException
from contextlib import closing

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('application/json') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them.
    """
    print(e)

def set_jira_uri_site_url(jira_uri, site_url):
    return jira_uri.replace('<site-url>', site_url)

def set_jira_uri_resource_name(jira_uri, resource_name):
    return jira_uri.replace('<resource-name>', resource_name)

def set_jira_uri(general_jira_uri, site_url, resource_name):
    jira_uri = set_jira_uri_site_url(general_jira_uri, site_url)
    jira_uri = set_jira_uri_resource_name(jira_uri, resource_name)
    return jira_uri