from trello_server import get_trello_data
import sys

my_boards = sys.argv[1].split(',')
personal_key = sys.argv[2]
personal_token = sys.argv[3]
filter_type = sys.argv[4]
my_team = (filter_type == 'team' and sys.argv[5].split(',')) or []
my_labels = (filter_type == 'label' and sys.argv[6].split(',')) or []

get_trello_data(my_boards, my_team, my_labels, filter_type, personal_key, personal_token)