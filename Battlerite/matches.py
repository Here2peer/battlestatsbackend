import requests, json
from Battlerite import players
from cfg.cfg import url, header

url = url + "matches" #url = "https://api.dc01.gamelockerapp.com/shards/global/matches"

#header = {
#    "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI3NzMxMGZjMC0yYjc1LTAxMzYtYjIyYi0wYTU4NjQ2MGI5M2QiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTI0NzQzMjI1LCJwdWIiOiJzdHVubG9jay1zdHVkaW9zIiwidGl0bGUiOiJiYXR0bGVyaXRlIiwiYXBwIjoiYmF0dGxlcml0ZS1jb21wYW5pb24tY2EzZmRmMTItODYxOS00ZDIzLWI3YWYtN2MyMWYzOGRkMjdlIiwic2NvcGUiOiJjb21tdW5pdHkiLCJsaW1pdCI6MTB9.hILjtng403GUUZN8cLqdsCp8R6qnESkoZOeLgRcvvx4",
#    "Accept": "application/vnd.api+json"
#}

def getMatchesInfo(playerName):
    query = {
        "sort": "-createdAt",
        "filter[playerIds]": players.getPlayerId(playerName),
        "page[limit]": "3"
    }

    request = requests.get(url, headers=header, params=query)
    request = request.json()
    return request


def getMatchesJson(playerName):
    query = {
        "sort": "-createdAt",
        "filter[playerName]":  players.getPlayerId(playerName)
    }

    r = requests.get(url, headers=header, params=query)
    f = r.json()
    return json.dumps(f)


def getTeams(playerName):
    match_info = parse_matches_info(getMatchesInfo(playerName))
    matches = match_info[0]
    rosters = match_info[1]
    player_ids = match_info[2]

    new_matches = []
    for match in matches:
        new_match = {}
        new_match['teams'] = []
        for roster in match['rosters']:
            new_team = {}
            new_team['won'] = rosters[roster]['won']
            new_team['players']=[]
            for roster_player_id in rosters[roster]['players']:
                new_team['players'].append(player_ids[roster_player_id])
            new_match['teams'].append(new_team)
        new_matches.append(new_match)
    return new_matches

def parse_matches_info(match_list):
    matches = []
    rosters = {}
    player_ids = {}

    for asset in match_list['data']:
        if asset["type"] == "match":
            match = {}
            match['type'] = asset['type']
            match['id'] = asset['id']
            match['rosters'] = []
            for roster in asset['relationships']['rosters']['data']:
                match['rosters'].append(roster['id'])
            matches.append(match)

    for asset in match_list["included"]:
        if asset["type"] == "roster":
            roster = {}
            roster['type'] = asset['type']
            roster['players'] = []
            roster['won'] = asset['attributes']['won']
            for participant in asset["relationships"]["participants"]["data"]:
                roster['players'].append(participant["id"])
            rosters[asset['id']] = roster

        elif asset["type"] == "participant":
            roster_player_id = asset['id']
            real_player_id = asset['relationships']['player']['data']['id']
            player_ids[roster_player_id] = real_player_id

    return [matches, rosters, player_ids]
