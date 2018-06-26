import requests, json
from Battlerite import players
from cfg.cfg import url, header

url = url + 'teams'


def getTeamInfo(id, playerName):
    if not id:
        playerName = players.getPlayerId(playerName)

    query = {
        "tag[playerIds]": playerName,
        "tag[season]": 6
    }

    request = requests.get(url, headers=header, params=query)
    try:
        request = request.json()
    except ValueError:  # includes simplejson.decoder.JSONDecodeError
        print('Decoding JSON has failed -- ***********************************')
        print('request: ' + str(request.content))
        return json.load(open('Battlerite/dummyJsons/faketeam.json', 'r'))
    try:
        team_data = request['data']
        return insertTeamMemberNames(team_data)
    except KeyError as error:
        print("KeyError")
        return request


# find team_id with playernames entered in the params
def team_id_with_playernames(player1, player2=None, player3=None):
    team_info = getTeamInfo(False, player1)
    team_found = False
    team_id = -1
    if player2 is not None:
        for team in team_info:
            member_names = []
            for name in team['attributes']['member_names'].values():
                member_names.append(name.replace(",", ''))
            if player2 in member_names :
                if player3 is not None:
                    if player3 in member_names:
                        team_found = True
                        team_id = team['id']
                else:
                    team_found = True
                    team_id = team['id']
            if team_found:
                break
    else:
        for team in team_info:
            if len(team['attributes']['members']) == 1:
                return team['id']
    return team_id


# create a dictionary for each team, where for each player in the team playerID is matched with playerName
# method retrieves player names in groups of 6
def insertTeamMemberNames(team_data):
    all_teammates = collect_team_member_ids(team_data)
    all_members = {}
    for id in all_teammates:
        pass
    all_teammates_jsons = []
    for id_list in all_teammates:  # for each unique team member fetch player info in one large dictionary
        if id_list != '':
            all_teammates_jsons.append(players.getPlayerInfo(1, id_list, True))


    for playerData in all_teammates_jsons:  # for each player match id with name
        last_player = playerData['data'][len(playerData['data']) - 1]
        for player in playerData['data']:
            player_name = player['attributes']['name']
            if player_name == last_player['attributes']['name']:
                all_members[player['id']] = player_name  # find name with id
            else:
                all_members[player['id']] = player_name + ','  # add comma for frontend purposes
    for team in team_data:  # create custom dictionary to add to team jsons containing playernames with id's
        members = {}
        team_members = team['attributes']['stats']['members']  # collect member ID's of team in a list
        for member in team_members:
            try:
                members[member] = all_members[member]  # find name with id
            except KeyError:
                members[member] = "Error: Api overloaded"
        team['attributes']['stats']['member_names'] = members
    return team_data


# collect all the different team member's id's in a list.
# id's are grouped by 6, because this is the limit of the amount of players information can be fetched from in one call.
def collect_team_member_ids(team_data):
    all_teammates = []  # prepare a list for strings
    processedIDS = []  # only save unique id's
    player_to_be_processed = 1
    for team in team_data:  # for every team
        team_members = team['attributes']['stats']['members']  # collect member ID's of team in a list
        for member in team_members:  # collect each member
            if member not in processedIDS:  # skip this step for preprocessed players
                if player_to_be_processed % 6 == 0:
                    member_string = member
                else:
                    member_string = member + ','

                teammate_list_index = int((player_to_be_processed - 1) / 6)
                if teammate_list_index == len(all_teammates):
                    all_teammates.append('')
                all_teammates[teammate_list_index] += member_string
                processedIDS.append(member)
                player_to_be_processed += 1

    last_id_string = all_teammates[int((player_to_be_processed - 2) / 6)]
    if last_id_string[-1] == ',':  # remove last comma if present
        all_teammates[int((player_to_be_processed - 2) / 6)] = last_id_string[:-1]
    return all_teammates
