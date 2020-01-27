from github_server import get_github_repo_summary, print_repo_summary
import sys

ACCESS_TOKEN = sys.argv[1]
MY_REPO = sys.argv[2] or ''

prs = get_github_repo_summary(ACCESS_TOKEN, MY_REPO)
print_repo_summary(prs)