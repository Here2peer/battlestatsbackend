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
        "page[limit]": "1"
    }

    request = requests.get(url, headers=header, params=query)
    request = request.json()
    return request

def getLastThreeMatches(playerName):
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


def getPlayerMatches():

    assetIdTest = "288039dd-4961-11e8-a3c8-0a586460b906"
    assetID = getMatchesInfo()["included"]
    assetsArray = []

    for asset in assetID:
        if asset["type"] == "asset":
            assetsArray.append(asset["id"])

    poep = assetsArray

    for assetje in poep:
        if assetje == assetIdTest:
            return str(poep.index(assetje))

def getWinningTeam(playerName):

    matches = getLastThreeMatches(playerName)
    IDs1 = []
    IDs2 = []
    IDs3 = []

    team1score = 0
    team2score = 0

    team1 = 0
    team2 = 0

    match1 = matches["data"][0]
    match2 = matches["data"][1]
    match3 = matches["data"][1]

    for round in match1["relationships"]["rounds"]["data"]:
         IDs1.append(round["id"])

    for round in match2["relationships"]["rounds"]["data"]:
         IDs2.append(round["id"])

    for round in match3["relationships"]["rounds"]["data"]:
         IDs3.append(round["id"])

    for ID in IDs1:
        for round in matches["included"]:
            if round["type"] == "round" and round["id"] == ID:
                if round["attributes"]["stats"]["winningTeam"] == 1:
                    team1 = team1 + 1
                else:
                    team2 = team2 + 1

            if team1 > team2:
                team1score = team1score + 1
            else:
                team2score = team2score + 1

    for ID in IDs2:
        for round in matches["included"]:
            if round["type"] == "round" and round["id"] == ID:
                if round["attributes"]["stats"]["winningTeam"] == 1:
                    team1 = team1 + 1
                else:
                    team2 = team2 + 1

            if team1 > team2:
                team1score = team1score + 1
            else:
                team2score = team2score + 1

    for ID in IDs3:
        for round in matches["included"]:
            if round["type"] == "round" and round["id"] == ID:
                if round["attributes"]["stats"]["winningTeam"] == 1:
                    team1 = team1 + 1
                else:
                    team2 = team2 + 1

            if team1 > team2:
                team1score = team1score + 1
            else:
                team2score = team2score + 1

    if team1score > team2score:
        return "1"
    else:
        return "2"