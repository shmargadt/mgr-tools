from setup import simple_get
from xlsx_importer import open_xlsx_file_and_return_workbook, write_to_xlsx, close_xlsx_file
import json
import pprint
pp = pprint.PrettyPrinter(depth=6)

def get_trello_boards(personal_key, personal_token):
    """Get all trello boards of user

    Parameters:
        personal_key (string): Personal developer API key of trello user.
        personal_token (string): Generated Token of trello user.

    Returns:
        boards (dict): trello boards of user, board id as a key and board name as a value.
                       F.E. {'ytNr5B5o9': 'New Board'}
        Or raising an error if http is failing

    """
    trello_url = 'https://api.trello.com/1/members/me/boards?key=' + personal_key + '&token=' + personal_token
    response = simple_get(trello_url)
    trello_boards_as_json = json.loads(response)
    boards = dict()
    for trello_card in trello_boards_as_json:
        boards[trello_card['shortLink']] = trello_card['name']
    return boards

    # Raise an exception if we failed to get any data from the url
    raise Exception('Error retrieving contents at {}'.format(trello_url))


def get_trello_board_data(board_id, personal_key, personal_token):
    """Get all data for one trello board of user

    Parameters:
        board_id (string): The id of a board as trello saving it.
        personal_key (string): Personal developer API key of trello user.
        personal_token (string): Generated Token of trello user.

    Returns:
        trello_board_as_json (json): Return the id and the name of the trello board in a json
        Or raising an error if http is failing

    """
    trello_url = 'https://api.trello.com/1/boards/' + board_id + '?fields=name,url&key=' + personal_key + '&token=' + personal_token
    response = simple_get(trello_url)
    trello_board_as_json = json.loads(response)
    return trello_board_as_json

    # Raise an exception if we failed to get any data from the url
    raise Exception('Error retrieving contents at {}'.format(trello_url))

def get_trello_board_cards_data(board_id, members_names, my_team, labels, filter_type, list_names, personal_key, personal_token):
    """Get all relevant data from trello board cards

    Parameters:
        board_id (string): The id of a board as trello saving it.
        members_names (dict): All the members names of the board,
                              member id as a key and member name as a value. F.e. {'TxCogm4e0rI': 'Tomer'}
        my_team (array): The names of the relevant trello members to look if they assigned to card.
        labels (string): The relevant label to look for.
        filter_type (string): Can be 'Team' or 'Label', it will decide the type of flitering by.
        list_names (dict): All the list (columns) of the board,
                           column id as a key and column name as a value. F.e. {'To19302Do': 'To Do'}
        personal_key (string): Personal developer API key of trello user.
        personal_token (string): Generated Token of trello user.

    Returns:
        sorted_array_of_parsed_cards (array): Return array of meaningful data of cards:
                                              members, name, url, column.
                                              sorted by column value
        Or raising an error if http is failing
    """
    array_of_parsed_cards = list()
    trello_url = 'https://api.trello.com/1/boards/' + board_id + '/cards?key=' + personal_key + '&token=' + personal_token
    response = simple_get(trello_url)
    # make it valid JSON
    trello_cards_as_json = json.loads(response)
    for trello_card in trello_cards_as_json:
        parsed_card = {}
        parsed_card['members'] = list()
        parsed_card['labels'] = list()
        is_team_card = False
        is_label_card = False
        for members_id in trello_card['idMembers']:
            if members_names[members_id] in my_team:
                is_team_card = True
                parsed_card['members'].append(members_names[members_id])
        for label in trello_card['labels']:
            parsed_card['labels'].append(label['name'])
            if label['name'] in labels:
                is_label_card = True
        if (not is_team_card and filter_type == 'team') or (not is_label_card and filter_type == 'label'):
            continue
        parsed_card['column'] = list_names[trello_card['idList']]
        parsed_card['name'] = trello_card['name']
        parsed_card['url'] = trello_card['url']
        array_of_parsed_cards.append(parsed_card)
    sorted_array_of_parsed_cards = sorted(array_of_parsed_cards, key=lambda k: k['column']) 
    return sorted_array_of_parsed_cards

    # Raise an exception if we failed to get any data from the url
    raise Exception('Error retrieving contents at {}'.format(trello_url))

def get_trello_board_lists_data(board_id, personal_key, personal_token):
    """Get all lists of one trello board

    Parameters:
        board_id (string): The id of a board as trello saving it.
        personal_key (string): Personal developer API key of trello user.
        personal_token (string): Generated Token of trello user.

    Returns:
        list_names (dict): Return dictionary of columns.
                           Column id as a key and column name as a value. F.e. {'To19302Do': 'To Do'}
        Or raising an error if http is failing
    """
    list_names = {}
    trello_url = 'https://api.trello.com/1/boards/' + board_id + '/lists?key=' + personal_key + '&token=' + personal_token
    response = simple_get(trello_url)
     # make it valid JSON
    trello_lists_as_json = json.loads(response)
    for trello_list in trello_lists_as_json:
        list_names[trello_list['id']] = trello_list['name']
    return list_names

    # Raise an exception if we failed to get any data from the url
    raise Exception('Error retrieving contents at {}'.format(trello_url))

def get_trello_board_members_data(board_id, personal_key, personal_token):
    """Get all members of one trello board

    Parameters:
        board_id (string): The id of a board as trello saving it.
        personal_key (string): Personal developer API key of trello user.
        personal_token (string): Generated Token of trello user.

    Returns:
        members_names (dict): Return dictionary of members.
                           Member id as a key and member name as a value. F.e. {'TxCogm4e0rI': 'Tomer'}
        Or raising an error if http is failing
    """
    members_names = {}
    trello_url = 'https://api.trello.com/1/boards/' + board_id + '/members?key=' + personal_key + '&token=' + personal_token
    response = simple_get(trello_url)
     # make it valid JSON
    trello_members_as_json = json.loads(response)
    for trello_member in trello_members_as_json:
        members_names[trello_member['id']] = trello_member['fullName']
    return members_names

    # Raise an exception if we failed to get any data from the url
    raise Exception('Error retrieving contents at {}'.format(trello_url))

def get_trello_data(boards, team, labels, filter_type, personal_key, personal_token):
    """Get all relevant data of trello and export it into xlsx file

    Parameters:
        boards (array): All id's of relevant trello boards.
        team (array): The names of the relevant trello members to look if they assigned to card.
        labels (string): The relevant label to look for.
        filter_type (string): Can be 'Team' or 'Label', it will decide the type of flitering by.
        personal_key (string): Personal developer API key of trello user.
        personal_token (string): Generated Token of trello user.

    Returns:
        all_trello_data (dict): Return dictionary of trello board data.
                                Trello board name as a key and Trello board data as a value. 
                                F.e. {'New Board': [
                                                    {
                                                       members: ['Tomer1', 'Meitale2']
                                                       column: 'Done' 
                                                       url: 'https://trello.com/b/Great2Work/565-make-life'
                                                       name: 'make life' 
                                                    }]}
        Or raising an error if http is failing
    """
    members_names = {}
    list_names = {}
    trello_data = []
    workbook = open_xlsx_file_and_return_workbook()
    worksheet = workbook.add_worksheet()
    
 
    all_trello_data = dict()
    row = 1
    for board_id in boards:
        trello_board_name = get_trello_board_data(board_id, personal_key, personal_token)['name']
        members_names = get_trello_board_members_data(board_id, personal_key, personal_token)
        list_names = get_trello_board_lists_data(board_id, personal_key, personal_token)
        one_board_trello_data = get_trello_board_cards_data(board_id, members_names, team, labels, filter_type, list_names, personal_key, personal_token)
        if not one_board_trello_data:
            return
        all_trello_data[trello_board_name] = one_board_trello_data
        fieldnames = one_board_trello_data[0].keys
        options = { 
            'merge_format': workbook.add_format({
                'bold': 1,
                'border': 1,
                'align': 'center',
                'valign': 'vcenter',
                'fg_color': 'gray',
                'font_color': 'white'}),
            'red': workbook.add_format({'bg_color': 'red'}),
            'green': workbook.add_format({'bg_color': 'green'}),
            'yellow': workbook.add_format({'bg_color': 'yellow'})
            }
        row = write_to_xlsx(worksheet, trello_board_name, fieldnames, one_board_trello_data, row, options)
    close_xlsx_file(workbook)
    return all_trello_data

