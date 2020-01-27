from trello_server import get_trello_data
import sys

my_boards = sys.argv[1].split(',')
personal_key = sys.argv[2]
personal_token = sys.argv[3]
my_team = sys.argv[4].split(',') or []
if len(sys.argv) > 5:  
    remove_column_flag = sys.argv[5].split(',')
else:
    remove_column_flag = ''
get_trello_data(my_boards, my_team, remove_column_flag, personal_key, personal_token)