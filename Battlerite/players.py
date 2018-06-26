import traceback

import requests, json
import sys

from cfg.cfg import url, header
from Database.ORM import player as player_base

url = url + "players"  # url = "https://api.dc01.gamelockerapp.com/shards/global/players"


def getPlayerInfo(id, playerName, list, steam_id=False):
    if id:
        query = {
            "filter[playerIds]": playerName,
            "page[limit]": "6"
        }
    else:
        query = {
            "filter[playerNames]": playerName,
            "page[limit]": "6"
        }
    if steam_id:
        query = {
            "filter[steamIds]": playerName,
            "page[limit]": "6"
        }
    request = requests.get(url, headers=header, params=query)
    try:
        request = request.json()
        for player in request['data']:
            custom_stats = {}
            stats = player['attributes']['stats']

            keylist = ['8', '2', '3']
            for key in keylist:
                try:
                    stats[key]
                except KeyError as error:
                    exc_info = sys.exc_info()
                    print(error)
                    stats[key] = 1
                    traceback.print_exception(*exc_info)

            time_played = int(stats['8'])
            hours_played = int(time_played / 60 / 60)
            wins = int(stats['2'])
            losses = int(stats['3'])
            custom_stats['timePlayed'] = str(hours_played) + "h"
            custom_stats['winRate'] = str(round(wins / (wins + losses) * 100.0, 1)) + '%'
            player['attributes']['customstats'] = custom_stats
            if not steam_id:
                player_base.update_player(player)
            else:
                player_base.update_player(player, )  # todo add some steam shizzle)
                # todo richard dit is jouw moment
    except ValueError:  # includes simplejson.decoder.JSONDecodeError
        print('Decoding JSON has failed -- ***********************************')
        print(str(request.content))
        with open('Battlerite/dummyJsons/failed.txt', 'w') as failedjson:
            failedjson.write(str(request.content))
        return json.load(open('Battlerite/dummyJsons/fakePLayer.json', 'r'))

    return request


def getAllPlayers():
    return player_base.getAllPlayers()


def delete_players():
    return player_base.clearAllPLayers()


def getPlayerJson(playerName):
    query = {
        "filter[playerNames]": playerName,
        "page[limit]": "3"
    }

    r = requests.get(url, headers=header, params=query)
    f = r.json()
    return json.dumps(f)


# get a player id by its battlerite name
def getPlayerId(playerName):
    player = player_base.get_player_by_name(playerName)
    if player is not None:
        if player.battlerite_id != -1:
            return player.battlerite_id
    playerId = getPlayerInfo(0, playerName, False)["data"][0]["id"]
    return playerId


# get a player name by its battlerite id
def getPlayerName(id):
    player = player_base.get_player_by_id(id)
    if player is not None:
        if player.battlerite_name != 'ERROR: player not found':
            if player.battlerite_name == 'Error: Api overloaded':
                print('trying battlerite api to get oplayername')
                return getPlayerInfo(1, id, False)["data"][0]["attributes"]['name']
            return player.battlerite_name
    return getPlayerInfo(1, id, False)["data"][0]["attributes"]['name']
