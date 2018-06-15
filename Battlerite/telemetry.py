import requests,json
from Battlerite import players, matches
from cfg.cfg import url, header

url = "https://cdn.gamelockerapp.com/stunlock-studios-battlerite/global/2018/05/02/17/07/55dea46c-4e2b-11e8-a3c8-0a586460b906-telemetry.json"

#header = {
#    "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI3NzMxMGZjMC0yYjc1LTAxMzYtYjIyYi0wYTU4NjQ2MGI5M2QiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTI0NzQzMjI1LCJwdWIiOiJzdHVubG9jay1zdHVkaW9zIiwidGl0bGUiOiJiYXR0bGVyaXRlIiwiYXBwIjoiYmF0dGxlcml0ZS1jb21wYW5pb24tY2EzZmRmMTItODYxOS00ZDIzLWI3YWYtN2MyMWYzOGRkMjdlIiwic2NvcGUiOiJjb21tdW5pdHkiLCJsaW1pdCI6MTB9.hILjtng403GUUZN8cLqdsCp8R6qnESkoZOeLgRcvvx4",
#    "Accept": "application/vnd.api+json"
#}

def getTelemetryInfo():
    query = {
        "page[limit]": "3000"
    }

    request = requests.get(url, headers=header, params=query)
    request = request.json()
    return request

def getTelemetryJson():
    query = {
        "page[limit]": "3000"
    }

    r = requests.get(url, headers=header, params=query)
    f = r.json()
    return json.dumps(f)

def getKD():
    telemetry = getTelemetryInfo()
    matchStandings = []

    for asset in telemetry:
       if asset["type"] == "Structures.RoundFinishedEvent":
            matchStandings.append(asset)

    matchUserIDs = {}

    for player in matchStandings[0]["dataObject"]["playerStats"]:
        matchUserIDs[player["userID"]] = {"kills": 1, "deaths": 1, "KD": 1}

    for asset in matchStandings:
        for playerStats in asset["dataObject"]["playerStats"]:
            playerid = playerStats['userID']
            matchUserIDs[playerid]["kills"] = matchUserIDs[playerid]["kills"] + int(playerStats["kills"])
            matchUserIDs[playerid]["deaths"] = matchUserIDs[playerid]["deaths"] + int(playerStats["deaths"])
            if playerStats["deaths"] == 0:
                matchUserIDs[playerid]["KD"] = "∞"
            else:
                matchUserIDs[playerid]["KD"] = round(matchUserIDs[playerid]["kills"] / matchUserIDs[playerid]["deaths"], 1)

    return json.dumps(matchUserIDs)

def getWins():

    telemetry = getTelemetryInfo()
    team1 = 0
    team2 = 0

    for asset in telemetry:
       if asset["type"] == "Structures.RoundFinishedEvent":

            if asset["dataObject"]["winningTeam"] == 1:
                team1 = team1 + 1
            else:
                team2 = team2 + 1

    if team1 > team2:
        return "1"
    else:
        return "2"
