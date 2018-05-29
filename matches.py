import requests
import json
import players

global url
url = "https://api.dc01.gamelockerapp.com/shards/global/matches"


global header
header = {
    "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI3NzMxMGZjMC0yYjc1LTAxMzYtYjIyYi0wYTU4NjQ2MGI5M2QiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTI0NzQzMjI1LCJwdWIiOiJzdHVubG9jay1zdHVkaW9zIiwidGl0bGUiOiJiYXR0bGVyaXRlIiwiYXBwIjoiYmF0dGxlcml0ZS1jb21wYW5pb24tY2EzZmRmMTItODYxOS00ZDIzLWI3YWYtN2MyMWYzOGRkMjdlIiwic2NvcGUiOiJjb21tdW5pdHkiLCJsaW1pdCI6MTB9.hILjtng403GUUZN8cLqdsCp8R6qnESkoZOeLgRcvvx4",
    "Accept": "application/vnd.api+json"
}

def getMatchesInfo(playerId):
    query = {
        "sort": "createdAt",
        "filter[playerIds]": playerId
    }

    request = requests.get(url, headers=header, params=query)
    request = request.json()
    return request

def getMatchesJson(playerId):
    query = {
        "sort": "createdAt",
        "filter[playerIds]": playerId
    }

    r = requests.get(url, headers=header, params=query)
    f = r.json()
    return json.dumps(f)


def getPlayerMatches(match, playerID):

    assetIdTest = "19520047-4e39-11e8-b6f7-0a5864608818"
    assetID = getMatchesInfo(playerID)["included"]
    assetsArray = []

    for asset in assetID:
        if asset["type"] == "asset":
            assetsArray.append(asset["id"])

    poep = assetsArray

    for assetje in poep:
        if assetje == assetIdTest:
            return str(poep.index(assetje))