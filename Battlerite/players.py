import requests, json
from cfg.cfg import url, header
url = url + "players" #url = "https://api.dc01.gamelockerapp.com/shards/global/players"

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
    try:
        request = request.json()
        for player in request['data']:
            custom_stats = {}
            stats = player['attributes']['stats']
            time_played = int(stats['8'])
            hours_played = int(time_played / 60 / 60)
            wins = int(stats['2'])
            losses = int(stats['3'])
            custom_stats['timePlayed'] = str(hours_played) + "h"
            custom_stats['winRate'] = str(round(wins / (wins + losses) * 100.0, 1)) + '%'
            player['attributes']['customstats'] = custom_stats

    except ValueError:  # includes simplejson.decoder.JSONDecodeError
        print('Decoding JSON has failed -- ***********************************')
        print(str(request.content))
        with open('dummyJsons/failed.txt', 'w') as failedjson:
            failedjson.write(str(request.content))
        return json.load(open('dummyJsons/fakePLayer.json', 'r'))


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
