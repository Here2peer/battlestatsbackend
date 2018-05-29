import requests
import json

global url
url = "https://api.dc01.gamelockerapp.com/shards/global/players"


global header
header = {
    "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI3NzMxMGZjMC0yYjc1LTAxMzYtYjIyYi0wYTU4NjQ2MGI5M2QiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTI0NzQzMjI1LCJwdWIiOiJzdHVubG9jay1zdHVkaW9zIiwidGl0bGUiOiJiYXR0bGVyaXRlIiwiYXBwIjoiYmF0dGxlcml0ZS1jb21wYW5pb24tY2EzZmRmMTItODYxOS00ZDIzLWI3YWYtN2MyMWYzOGRkMjdlIiwic2NvcGUiOiJjb21tdW5pdHkiLCJsaW1pdCI6MTB9.hILjtng403GUUZN8cLqdsCp8R6qnESkoZOeLgRcvvx4",
    "Accept": "application/vnd.api+json"
}

def getPlayerInfo(playerName):
    query = {
        "filter[playerNames]": playerName,
        "page[limit]": "3"
    }
    request = requests.get(url, headers=header, params=query)
    request = request.json()
    customStats = {}
    customStats['timePlayed'] = "hoi"
    customStats['winRate'] = "hpoi"
    request['data'][0]['attributes']['customstats'] = customStats
    return request

def getPlayerJson(playerName):
    query = {
        "filter[playerNames]": playerName,
        "page[limit]": "3"
    }

    r = requests.get(url, headers=header, params=query)
    f = r.json()
    return json.dumps(f)

def getPlayerId(playerName):

    playerId = getPlayerInfo(playerName)["data"][0]["id"]
    return playerId