import requests
import json
import players

def getURL(player):
    global url
    playerString = ""
    for pl in player:
        playerString += players.getPlayerId(pl)
        if pl != player[len(player) - 1]:
            playerString += ","
    print(playerString)
    url = "https://api.dc01.gamelockerapp.com/shards/global/teams?tag[season]=2&tag[playerIds]=" + playerString
    print(url)
    return url


global header
header = {
    "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI3NzMxMGZjMC0yYjc1LTAxMzYtYjIyYi0wYTU4NjQ2MGI5M2QiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTI0NzQzMjI1LCJwdWIiOiJzdHVubG9jay1zdHVkaW9zIiwidGl0bGUiOiJiYXR0bGVyaXRlIiwiYXBwIjoiYmF0dGxlcml0ZS1jb21wYW5pb24tY2EzZmRmMTItODYxOS00ZDIzLWI3YWYtN2MyMWYzOGRkMjdlIiwic2NvcGUiOiJjb21tdW5pdHkiLCJsaW1pdCI6MTB9.hILjtng403GUUZN8cLqdsCp8R6qnESkoZOeLgRcvvx4",
    "Accept": "application/vnd.api+json"
}

def getTeamInfo(*player):

    url = getURL(player)

    query = {
        "tag[playerIds]": "none"
    }

    request = requests.get(url, headers=header, params=query)
    request = request.json()

    team_data = request["data"]
    return fetchTeamMemberNames(team_data)


def fetchTeamMemberNames(team_data):
    processedIDS = {}  # don't fetch players twice!
    for team in team_data:  # for every team
        members = {}
        team_members = team['attributes']['stats']['members']  # collect member ID's of team in a list
        # todo create database of playernames - id's bcz fetching it all takes too long/raises errors
        for member in team_members:
            if member not in processedIDS.keys():  # skip this step for preprocessed players
                members[member] = players.getPlayerInfo(1, member)['data'][0]['attributes']['name']  # find name with id
                processedIDS[member] = members[member]
            else:
                members[member] = processedIDS[member]

            if member != team_members[len(team_members) - 1]:  # add a , for all but the last name for frontend purposes
                members[member] += ', '

        team['attributes']['stats']['member_names'] = members
    return team_data


def getTeamJson(*player):

    url = getURL(player)
    query = {
        "tag[playerIds]": "none"
    }
    r = requests.get(url, headers=header, params=query)
    f = r.json()
    return json.dumps(f)
