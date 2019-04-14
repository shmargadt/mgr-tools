from trello_server import get_trello_boards, get_trello_data, get_trello_board_members_data
import pprint
pp = pprint.PrettyPrinter(depth=6)

def run_trello_gui_script(): 

    # General Introduction Text
    print("\033[1;36;40m=====================================\n Welcome for your trello status \n =====================================")
    print("\033[0;37;40mThis program get trello data from your boards and export it into xlsx file. \n It is using your unique key and token and don\'t store it. \n")
    
    # Auth data
    print("\033[1;32;40mLet's start - ")
    print("\033[0;37;40mGo to the Developer API Keys screen: https://trello.com/app-key \n")
    private_key = input("1. Copy the \033[1;37;40mKey \033[0;37;40mat the top of the page: ")
    private_token = input("2. Generate and copy the \033[1;37;40mToken\033[0;37;40m: ")
    
    # Board data
    pp.pprint(get_trello_boards(private_key, private_token))
    print('3. Please enter your Trello boards hash with quotes, one by one, united by a comma between each other. \n F.E.: TreLlo2,TrEllo2,tRellO3:')
    trello_boards = input("( it can be anyone from the list above) \n")
    my_boards = trello_boards.split(',')
    
    # Members/Label Data
    team_or_label = input("\033[0;33;40mDo you look for your team status or specific label status? [T/L] ")
    my_team = None
    my_labels = []

    # Members Data
    if team_or_label == 'T' or team_or_label == 't': 
      filter_type = 'team'
      dest = dict() 
      for board_id in my_boards:
        board_members = get_trello_board_members_data(board_id, private_key, private_token)
        dest.update(board_members)
      pp.pprint(dest)
      trello_members = input("\033[0;37;40m4. Please enter your Trello members names with quotes, one by one, united by a comma between each other between each other. \n F.e. 'Tomer1','Meitale2','Roii3' \n" )
      my_team = trello_members.split(',')
    else: # Label Data
      filter_type = 'label'
      trello_label = input("\033[0;37;40m4. Please enter the label name or part of it: ")
      my_labels = trello_label


    # Run as a script line
    print("\n\n\033[93mThis line script will generate the data for the same settings:")
    line_of_script = "python trello_line_script.py " + ''.join(trello_boards) + " " + private_key + " " + private_token + " " + filter_type  + " " + ','.join(my_team)  + " " + ''.join(my_labels)
    print("\033[1;37;40m" + line_of_script)
    print("\n\033[92mPlease run the above command in order to genreate your excel file!\n")
    return

run_trello_gui_script()
