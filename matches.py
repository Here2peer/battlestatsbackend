import requests
import json

global url
url = "https://api.dc01.gamelockerapp.com/shards/global/matches"


global header
header = {
    "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI3NzMxMGZjMC0yYjc1LTAxMzYtYjIyYi0wYTU4NjQ2MGI5M2QiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTI0NzQzMjI1LCJwdWIiOiJzdHVubG9jay1zdHVkaW9zIiwidGl0bGUiOiJiYXR0bGVyaXRlIiwiYXBwIjoiYmF0dGxlcml0ZS1jb21wYW5pb24tY2EzZmRmMTItODYxOS00ZDIzLWI3YWYtN2MyMWYzOGRkMjdlIiwic2NvcGUiOiJjb21tdW5pdHkiLCJsaW1pdCI6MTB9.hILjtng403GUUZN8cLqdsCp8R6qnESkoZOeLgRcvvx4",
    "Accept": "application/vnd.api+json"
}

def getMatchesInfo():
    query = {
        "sort": "createdAt",
        "filter[playerIds]": 989458479959953408
    }

    request = requests.get(url, headers=header, params=query)
    request = request.json()
    return request

def getMatchesJson():
    query = {
        "sort": "createdAt",
        "filter[playerName]": "Joltz"
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