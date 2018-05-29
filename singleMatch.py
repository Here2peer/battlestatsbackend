import requests
import json
import players
import matches

def getMatch(match, playerID):
    global url
    url = "https://api.dc01.gamelockerapp.com/shards/global/matches/" + matches.getMatchLocation(match, playerID)

global header
header = {
    "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI3NzMxMGZjMC0yYjc1LTAxMzYtYjIyYi0wYTU4NjQ2MGI5M2QiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTI0NzQzMjI1LCJwdWIiOiJzdHVubG9jay1zdHVkaW9zIiwidGl0bGUiOiJiYXR0bGVyaXRlIiwiYXBwIjoiYmF0dGxlcml0ZS1jb21wYW5pb24tY2EzZmRmMTItODYxOS00ZDIzLWI3YWYtN2MyMWYzOGRkMjdlIiwic2NvcGUiOiJjb21tdW5pdHkiLCJsaW1pdCI6MTB9.hILjtng403GUUZN8cLqdsCp8R6qnESkoZOeLgRcvvx4",
    "Accept": "application/vnd.api+json"
}

def getMatchInfo(match, playerID):

    getMatch(match, playerID)

    query = {
        "sort": "createdAt",
    }

    request = requests.get(url, headers=header, params=query)
    request = request.json()
    return request

def getMatchJson(match, playerID):

    getMatch(match, playerID)

    query = {
        "sort": "createdAt",
    }

    r = requests.get(url, headers=header, params=query)
    f = r.json()
    return json.dumps(f)