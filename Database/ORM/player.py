from mongoengine import *


class Player(Document):
    battlerite_name = StringField(max_length=50)
    battlerite_id = IntField(max_value=100000000000000000000)
    steam_id = IntField()  # todo max steam id, letters allowed?

    winrate = StringField(max_length=10)
    time_played = IntField()
    twov2_ranked_wins = IntField()
    twov2_unranked_wins = IntField()
    threev3_ranked_wins = IntField()
    threev3_unranked_wins = IntField()


# update or create a player and save it to the database
def update_player(playerJson, steam_id=-1):
    br_name = playerJson['attributes']['name']
    br_id  = playerJson['id']
    stats = playerJson['attributes']['stats']
    player = get_player_by_name(br_name)
    if player is None and br_id != -1:
        player = get_player_by_id(br_id)
    if player is None and steam_id != -1:
        player = get_player_by_steam(steam_id)

    if player is not None:
        player.update(
            battlerite_name=br_name,
            battlerite_id=br_id,
            steam_id=steam_id,
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
            winrate=playerJson['attributes']['customstats']['winRate'],
            time_played=int(stats['8']),
            twov2_ranked_wins=int(stats['10']),
            twov2_unranked_wins=int(stats['14']),
            threev3_ranked_wins=int(stats['12']),
            threev3_unranked_wins=int(stats['16'])
        ).save()
        print('*********   created player   *********')


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
