import sys
import traceback

from mongoengine import *


class Player(Document):
    battlerite_name = StringField(max_length=50)
    battlerite_id = IntField(max_value=100000000000000000000)
    steam_id = IntField()  # todo max steam id, letters allowed?
    steam_profile = StringField(max_length=200)
    winrate = StringField(max_length=10)
    time_played = IntField()
    twov2_ranked_wins = IntField()
    twov2_unranked_wins = IntField()
    threev3_ranked_wins = IntField()
    threev3_unranked_wins = IntField()


# update or create a player and save it to the database
def update_player(playerJson, steam_id=-1, steam_pic="nopic"):
    br_name = playerJson['attributes']['name']
    br_id = playerJson['id']
    stats = playerJson['attributes']['stats']
    player = get_player_by_name(br_name)
    if player is None and br_id != -1:
        player = get_player_by_id(br_id)
    if player is None and steam_id != -1:
        player = get_player_by_steam(steam_id)

    # if value is 0 the battlerite api omits the stat, compensate that here
    keylist = ['8', '10', '14', '12', '16']
    for key in keylist:
        try:
            stats[key]
        except KeyError as error:
            exc_info = sys.exc_info()
            print(error)
            stats[key] = 0
            traceback.print_exception(*exc_info)


    if player is not None:
        player.update(
            battlerite_name=br_name,
            battlerite_id=br_id,
            steam_id=steam_id,
            steam_profile=steam_pic,
            winrate=playerJson['attributes']['customstats']['winRate'],
            time_played=int(stats['8']),
            twov2_ranked_wins=int(stats['10']),
            twov2_unranked_wins=int(stats['14']),
            threev3_ranked_wins=int(stats['12']),
            threev3_unranked_wins=int(stats['16'])
        )
        print('*********   updated player   *********')
    else:
        print(br_name + " " + str(br_id) + " " + str(steam_id))
        Player(
            battlerite_name=br_name,
            battlerite_id=br_id,
            steam_id=steam_id,
            steam_profile=steam_pic,
            winrate=playerJson['attributes']['customstats']['winRate'],
            time_played=int(stats['8']),
            twov2_ranked_wins=int(stats['10']),
            twov2_unranked_wins=int(stats['14']),
            threev3_ranked_wins=int(stats['12']),
            threev3_unranked_wins=int(stats['16'])
        ).save()
        print('*********   created player   *********')


# update steam info of a player in the database
def update_player_steam_info(battlerite_id, steam_id=-1, steam_pic="nopic"):
    br_id = battlerite_id
    player = get_player_by_id(br_id)
    if player is not None:
        player.update(
            steam_id=steam_id,
            steam_profile=steam_pic
        )
        print('*********   updated player   *********')
    else:
        return False
    return True


def print_player_info(player):
    print(player.battlerite_name + " " + str(player.battlerite_id) + " " + str(player.steam_id))


# retrieve a player from the database
def get_player_by_name(playername):
    query_set = Player.objects(battlerite_name=playername)
    if query_set.count() > 0:
        for player in query_set:
            return player
    else:
        return None


# retrieve a player from the database
def get_player_by_id(id):
    query_set = Player.objects(battlerite_id=id)
    if query_set.count() > 0:
        for player in query_set:
            return player
    else:
        return None


# retrieve a player from the database
def get_player_by_steam(steam):
    query_set = Player.objects(steam_id=steam)
    if query_set.count() > 0:
        for player in Player.objects(steam_id=steam):
            return player
    else:
        return None


def getAllPlayers():
    players = []
    for player in Player.objects:
        players.append(player)
    return players


def clearAllPLayers():
    players = []
    for player in Player.objects:
        players.append(player)
        player.delete()
    return players
