import requests
import json

global url
url = "https://api.dc01.gamelockerapp.com/shards/global/players"


global header
header = {
    "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI3NzMxMGZjMC0yYjc1LTAxMzYtYjIyYi0wYTU4NjQ2MGI5M2QiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTI0NzQzMjI1LCJwdWIiOiJzdHVubG9jay1zdHVkaW9zIiwidGl0bGUiOiJiYXR0bGVyaXRlIiwiYXBwIjoiYmF0dGxlcml0ZS1jb21wYW5pb24tY2EzZmRmMTItODYxOS00ZDIzLWI3YWYtN2MyMWYzOGRkMjdlIiwic2NvcGUiOiJjb21tdW5pdHkiLCJsaW1pdCI6MTB9.hILjtng403GUUZN8cLqdsCp8R6qnESkoZOeLgRcvvx4",
    "Accept": "application/vnd.api+json"
}

def getPlayerInfo(id, playerName):
    if id:
        query = {
            "filter[playerIds]": playerName,
            "page[limit]": "3"
        }
    else:
        query = {
            "filter[playerNames]": playerName,
            "page[limit]": "3"
        }
    request = requests.get(url, headers=header, params=query)
    #  print(request.text)
    try:
        request = request.json()

        custom_stats = {}
        stats = request['data'][0]['attributes']['stats']
        time_played = int(stats['8'])
        hours_played = int(time_played / 60 / 60)
        wins = int(stats['2'])
        losses = int(stats['3'])
        custom_stats['timePlayed'] = str(hours_played) + "h"
        custom_stats['winRate'] = str(round(wins / (wins + losses) * 100.0, 1)) + '%'
        request['data'][0]['attributes']['customstats'] = custom_stats

    except ValueError:  # includes simplejson.decoder.JSONDecodeError
        print('Decoding JSON has failed -- ***********************************')
        return json.load(open('fakePLayer.json', 'r'))


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
    playerId = getPlayerInfo(0, playerName)["data"][0]["id"]
    return playerId