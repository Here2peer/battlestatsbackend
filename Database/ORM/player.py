from mongoengine import *


class Player(Document):
    battlerite_name = StringField(max_length=50)
    battlerite_id = IntField(max_value=100000000000000000000)
    steam_id = IntField()  # todo max steam id, letters allowed?


# update or create a player and save it to the database
def update_player(br_name='ERROR: player not found', br_id=-1, steam_id=-1):
    playername_set = False
    player_id_set = False
    steam_id_set = False

    player = get_player_by_name(br_name)
    if player is None and br_id != -1:
        player = get_player_by_id(br_id)
    if player is None and steam_id != -1:
        player = get_player_by_steam(steam_id)

    if player is not None:
        if player.battlerite_name != 'ERROR: player not found':
            playername_set = True
        if player.battlerite_id != -1:
            player_id_set = True
        if player.steam_id != -1:
            steam_id_set = True

        print_player_info(player)
        do_update = False
        if (br_name != 'ERROR: player not found' and not playername_set) and br_name != player.battlerite_name:
            player.battlerite_name = br_name
            do_update = True
        if (br_id != -1 and not player_id_set) and br_id != player.battlerite_id:
            player.battlerite_id = br_id
            do_update = True
        if (steam_id != -1 and not steam_id_set) and steam_id != player.steam_id:
            player.steam_id = steam_id
            do_update = True

        if do_update:
            print('*********   updated player   *********')
            print(br_name + " " + str(br_id) + " " + str(steam_id))
            player.update()
    else:
        print(br_name + " " + str(br_id) + " " + str(steam_id))
        Player(
            battlerite_name=br_name,
            battlerite_id=br_id,
            steam_id=steam_id,
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
    query_set = Player.objects(steam_id = steam)
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
