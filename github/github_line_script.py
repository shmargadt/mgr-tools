from github_server import get_github_data, print_github_data
import sys

ACCESS_TOKEN = sys.argv[1]
MY_TEAM = sys.argv[2].split(',') or []

prs = get_github_data(ACCESS_TOKEN, MY_TEAM)
print_github_data(prs)